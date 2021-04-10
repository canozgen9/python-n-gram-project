import re
import time
from pathlib import Path
from nltk.util import ngrams
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')


def to_lower_case(word):
    lower_map = {
        ord(u'I'): u'ı',
        ord(u'İ'): u'i',
    }
    return word.translate(lower_map).lower()


def build_n_gram_map(n, words):
    map = {}
    wordList = list(ngrams(words, n))
    for x in wordList:
        key = ' '.join(x)

        if key in map:
            map[key] = map[key] + 1
        else:
            map[key] = 1

    return dict(sorted(map.items(), key=lambda item: item[1], reverse=True))


def prepare_output(file_name, n, words, output_dir):
    outputFile = open(f'{output_dir}/{file_name}-{n}-gram.txt', 'w')
    map = build_n_gram_map(n, words)
    for word in map:
        count = map[word]
        outputFile.write(f'{count}: {word}\n')
    outputFile.close()


if __name__ == '__main__':
    # python 3
    total_n_s = 3
    input_dir = './assets'
    output_dir = './outputs'

    allClearWords = []
    logs = []
    a_start = time.time()
    for path in Path(f'{input_dir}').rglob('*.txt'):
        f_start = time.time()
        input_file_name = f'single-{path.parent.parent.name}-{path.parent.name}-{path.name}'
        print(f'reading {input_file_name}')
        file = open(path.absolute(), "r+")
        fileContent = file.read()
        file.close()
        words = fileContent.split()
        clearWords = []
        for word in words:
            clearWord = to_lower_case(re.sub("[^\w\s]", "", word))
            if len(clearWord) > 0:
                clearWords.append(clearWord)
                allClearWords.append(clearWord)

        for n in range(1, total_n_s + 1):
            n_start = time.time()
            prepare_output(input_file_name, n, clearWords, output_dir=output_dir)
            n_end = time.time()
            n_elapsed = n_end - n_start
            logs.append(f'{input_file_name}-{n}-gram: {n_elapsed}')
            print(f'{input_file_name}-{n}-gram: {n_elapsed}')

        f_end = time.time()
        f_elapsed = f_end - f_start
        logs.append(f'{input_file_name}-total: {f_elapsed}')
        print(f'{input_file_name}-total: {f_elapsed}')
    for n in range(1, total_n_s + 1):
        print(f'starting all-{n}-gram')
        n_start = time.time()
        prepare_output('all', n, allClearWords, output_dir=output_dir)
        n_end = time.time()
        n_elapsed = n_end - n_start
        logs.append(f'all-{n}-gram: {n_elapsed}')
        print(f'all-{n}-gram: {n_elapsed}')

    a_end = time.time()
    a_elapsed = a_end - a_start
    logs.append(f'all-total: {a_elapsed}')
    print(f'all-total: {a_elapsed}')

    logFile = open(f'{output_dir}/log.txt', "w")
    for log in logs:
        logFile.write(f'{log}\n')
    logFile.close()

    print("all done!")
    exit()
