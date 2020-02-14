from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
import json
import nltk
import random
import sqlite3

# Install NLTK prerequisites
nltk.download('punkt')
nltk.download('stopwords')

# establish db connection
conn = sqlite3.connect('books.db')


def query_data(query):
    '''
    Executes a given query and returns data from the database.
    '''
    return conn.cursor().execute(query).fetchall()


def update_data(query, params):
    '''
    Executes a given query and updates data on the database.
    '''
    conn.cursor().execute(query, params)
    # Shouldn't commit very often - lower performance.
    conn.commit()


def generate_keywords(data):
    '''
    Generates a set of keywords given a string.
    Removes all punctuation, performs tokenization,
    stopword removal and stemming(Porter).
    '''
    # check if row data is not null
    if(data != None):
        # Remove puncuation
        data_list = RegexpTokenizer(r'\w+').tokenize(data)
        data_str = ' '.join(data_list)

        # Tokenize
        tokens = word_tokenize(data_str)

        # StopWord removal
        stop_words_en = set(stopwords.words('english'))
        # stop_words_es = set(stopwords.words('spanish'))

        filtered_tokens = [w.lower()
                           for w in tokens if not w.lower() in stop_words_en]
        # filtered_tokens = [w.lower() for w in tokens if not w.lower() in stop_words_es]

        # Stemming
        ps = PorterStemmer()
        keywords = [ps.stem(w) for w in filtered_tokens]

        return list(dict.fromkeys(keywords))
    else:
        return list(dict.fromkeys(''))


def init_pre_processing():
    # checks if the db is initialized
    try:
        conn.cursor().execute('SELECT keywords FROM "BX-Books";')
    except sqlite3.OperationalError:
        print('[#]\t`keyword` column doesn\'t exist.')
        print('[#]\tCreating additional `keyword` column.')
        conn.cursor().execute('ALTER TABLE "BX-Books" ADD "keywords" TEXT;')
        print('[#]\tRemoving books with < 10 ratings')
        query_data('DELETE FROM "BX-Books" WHERE "ISBN" IN (SELECT "ISBN" FROM "BX-Book-Ratings" br GROUP BY br."ISBN" HAVING count("ISBN") < 10);')

        print('[#]\tRemoving users who rated < 5 books')
        query_data('DELETE FROM "BX-Users" WHERE "User-ID" NOT IN (SELECT br."User-ID" FROM "BX-Book-Ratings" br GROUP BY br."User-ID" HAVING count(br."User-ID") > 5);')

        print('[#]\tInitializing pre-processing.')
        print('[#]\tGenerating keywords...')
        print('[#]\tThis may take a while due to dataset size.')
        for row in query_data('SELECT "ISBN", "Book-Title" FROM "BX-Books";'):
            keywords = generate_keywords(row[1])
            # Copy keywords to database
            update_data(
                'UPDATE `BX-Books` SET keywords = ? WHERE ISBN = ?;', (','.join(keywords), row[0]))
        print('[#]\tDone!\n')


def get_random_users():
    '''
    Selects 5 users pseudo-randomly
    '''
    data = query_data(
        'SELECT "User-ID" FROM "BX-Book-Ratings" WHERE ISBN IN (SELECT ISBN FROM "BX-Books") AND "User-ID" IN (SELECT "User-ID" from "BX-Users") GROUP BY "User-ID" HAVING count("User-ID") > 5;')

    return random.choices(data, k=5)


def create_profile(user_id: 'User ID', books: 'List of book ISBNs'):
    '''
    Creates a user profile combining keywords,
    authors and years of publication given the top 3 rated books of the user.
    '''
    user = {'user_id': '', 'keywords': '',
            'authors': '', 'years_of_publication': ''}
    # get book details
    for book in books:
        data = query_data(
            'SELECT keywords, "Book-Author", "Year-Of-Publication" FROM "BX-Books" WHERE ISBN = \'' + book[0] + '\';')
        user['user_id'] = user_id[0]
        user['keywords'] += data[0][0] + ','
        user['authors'] += data[0][1] + ','
        user['years_of_publication'] += data[0][2] + ','

    # lazy - remove last trailing comma
    user['keywords'] = user['keywords'][:-1]
    user['keywords'] = user['keywords'].split(',')
    user['authors'] = user['authors'][:-1]
    user['years_of_publication'] = user['years_of_publication'][:-1]

    return user


def jaccard_similarity(list_a: 'List A', list_b: 'List B'):
    '''
    Returns the Jaccard similarity between two lists of strings
    '''
    set_a = set(list_a)
    set_b = set(list_b)
    return float(len(set_a.intersection(set_b)) / len(set_a.union(set_b)))


def dice_coefficient(list_a: 'List A', list_b: 'List B'):
    set_a = set(list_a)
    set_b = set(list_b)
    return float(len(set_a.intersection(set_b)) * 2.0) / (len(set_a) + len(set_b))


def get_recommended_books(user_profile: 'User profile', jaccard: bool):
    '''
    Returns 10 recommended books based on the users profile.
    '''
    similarities = []
    unrated_books = query_data(
        'SELECT keywords,"Book-Author","Year-Of-Publication",ISBN,"Book-Title" FROM "BX-Books" WHERE ISBN NOT IN (SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID" = \'' + user_profile['user_id'] + '\');')

    for book in unrated_books:
        book_similarity = {'ISBN': '', 'title': '', 'similarity': ''}
        year_of_pub_diff = []
        author_similarity = 0
        keyword_similarity = 0
        book_similarity['ISBN'] = book[3]
        book_similarity['title'] = book[4]

        # solve edge case where year of publication data is invalid
        try:
            int(book[2])
        except ValueError:
            continue

        # calculate minimum difference of year of publication
        for year in user_profile['years_of_publication'].split(','):
            year_of_pub_diff.append(
                1 - (abs(int(year) - int(book[2])) / 2005))  # 1-(|a-b| / 2005)

        # calculate author similarity
        if(book[1] in user_profile['authors'].split(',')):
            if(jaccard == True):
                author_similarity = 0.4
            else:
                author_similarity = 0.3

        # check if we're doing jaccard or dice
        if(jaccard == True):
            keyword_similarity = jaccard_similarity(
                user_profile['keywords'], book[0].split(','))
            # set similarity
            book_similarity['similarity'] = (
                keyword_similarity * 0.2) + (author_similarity) + (min(year_of_pub_diff) * 0.4)
        else:
            keyword_similarity = dice_coefficient(
                user_profile['keywords'], book[0].split(','))
            # set dice coefficient
            book_similarity['similarity'] = (
                keyword_similarity * 0.5) + (author_similarity) + (min(year_of_pub_diff) * 0.2)

        similarities.append(book_similarity)

    # sort list and return top 10
    return sorted(similarities, key=lambda k: k['similarity'], reverse=True)[:10]


def save_recommendations(filename, user_profile, books):
    with open('' + filename + '.json', 'w') as fp:
        output = {'user': user_profile, 'recommendations': books}
        json.dump(output, fp, indent=4)


def calculate_overlap(recommended_books_jaccard, recommended_books_dice):
    '''
    Calculates overlap between Jaccard and Dice coefficient results
    '''
    jaccard_avg = float(sum(book['similarity']
                            for book in recommended_books_jaccard))

    dice_avg = float(sum(book['similarity']
                         for book in recommended_books_dice))

    return (jaccard_avg + dice_avg) / 20


def get_golden_standard(recommended_books_jaccard, recommended_books_dice):
    jaccard_frequency = Counter(book['ISBN']
                                for book in recommended_books_jaccard)
    dice_frequency = Counter(book['ISBN'] for book in recommended_books_dice)

    book_frequencies = (jaccard_frequency+dice_frequency).most_common()

    golden_standard = []

    # check equality of book frequency
    for isbn in book_frequencies:
        books = next(((book_jaccard, book_dice) for (book_jaccard, book_dice) in zip(recommended_books_jaccard,
                                                                                     recommended_books_dice) if book_jaccard['ISBN'] == isbn[0] or book_dice['ISBN'] == isbn[0]), None)

        # get book with biggest value of similarity
        book = max(books, key=lambda b: b['similarity'])
        golden_standard.append(book)
    return golden_standard


init_pre_processing()

users = get_random_users()

for user_id in users:
    # get top 3 rated books
    books = query_data('SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID"=\'' + user_id[0] +
                       '\' AND ISBN IN (SELECT ISBN FROM "BX-Books") ORDER BY "Book-Rating" DESC LIMIT 3;')

    print('\nGenerating profile for user_id: ' + user_id[0])
    user_profile = create_profile(user_id, books)

    print('Calculating recommended books')
    recommended_books_jaccard = get_recommended_books(
        user_profile, jaccard=True)

    recommended_books_dice = get_recommended_books(
        user_profile, jaccard=False)

    # overlap
    overlap = calculate_overlap(
        recommended_books_jaccard, recommended_books_dice)

    print('Results overlap by %.2f%% -- [%.10f]' % ((overlap * 100), overlap))

    # golden standard
    golden_standard = get_golden_standard(
        recommended_books_jaccard, recommended_books_dice)

    # jaccard overlap with golden standard
    gs_vs_jaccard = calculate_overlap(
        golden_standard, recommended_books_jaccard)
    print(
        'Jaccard Similarity vs Golden Standard overlap by %.2f%% -- [%.10f]' % ((gs_vs_jaccard * 100), gs_vs_jaccard))

    # dice coefficient overlap with golden standard
    gs_vs_dice = calculate_overlap(
        golden_standard, recommended_books_dice)
    print(
        'Dice Coefficient vs Golden Standard overlap by %.2f%% -- [%.10f]' % ((gs_vs_dice * 100), gs_vs_dice))

    print('Writing data to file...')
    save_recommendations(user_id[0] + '-jaccard',
                         user_profile, recommended_books_jaccard)
    save_recommendations(user_id[0] + '-dice',
                         user_profile, recommended_books_dice)
    print('Done!')

# terminate db connection
conn.close()
