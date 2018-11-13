from flask import Flask, request, jsonify, json
import pandas as pd
import numpy as np

app = Flask(__name__)

class PrefixTree:
    #Моя структура основана на каком то объекте и его рейтинге
    #Можно так же сделать по частоте встречаемости, только вместо рейтинга добавлять в значение конечной ноды частоту встречаемости, т.е. при добавлении, при попытке добавить уже существующую строку добавлять +1 к встречаемости и в последствии сортировать по этому значению, как я делаю сортировку по рейтингу
    
    def __init__(self):
        self.root = [{}]
        self.result = []
        self.word = []
        
    def add(self, string, rating):
        if self.check(string):
            return
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                wrk_dict[0][i] = [{}]
                wrk_dict = wrk_dict[0][i]
        wrk_dict.append(rating)
        
    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        if len(wrk_dict) != 1:
            return True
        return False
    
    def check_part(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True
            
    def go(self, wrk_dict, word):   #Метод для прохода всего дерева и закидывания конечных нод в результат
        if len(wrk_dict) == 2:
            self.result.append([''.join(word), wrk_dict[1]])
        if len(wrk_dict[0].keys()) == 1:
            letter = list(wrk_dict[0].keys())[0]
            word.append(letter)
            wrk_dict = wrk_dict[0][letter]
            self.go(wrk_dict, word)
        elif len(wrk_dict[0].keys()) >= 1:
            for letter in list(wrk_dict[0].keys()):
                word_new = list(word)
                word_new.append(letter)
                wrk_dict_new = wrk_dict[0][letter]
                self.go(wrk_dict_new, word_new)
        
    def search(self, string):
        self.result = []
        wrk_dict = self.root
        if self.check_part(string) == True:
            for i in string:
                self.word.append(i)
                wrk_dict = wrk_dict[0][i]
        else:
            return []
        self.go(wrk_dict, self.word)
        self.word = []
        return self.result
        
        
def init_prefix_tree(filename):
    # Спарсил немного топа игрулек с рейтингом, гружу игрульку и соответствующий ей рейтинг, чтобы выводить топ по рейтингу
    df = pd.read_csv(filename)
    data = {row['title']:row['rating'] for index, row in df.iterrows()}
    pr_tree = PrefixTree()
    keys = list(data.keys())
    values = list(data.values())
    for i in range(len(keys)):
        pr_tree.add(keys[i], values[i])
    return pr_tree

tree = init_prefix_tree('games.txt')

@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    string.capitalize() #Потому что все названия с заглавных букв ¯\_(ツ)_/¯
    if tree.check_part(string) == False:
        return '<b> <big><big><big><big><big><big><big><big>¯\_(ツ)_/¯</big></big></big></big></big></big></big></big> <br>Ничего не найдено. Проверьте правильность написания и попробуйте еще раз!<br>Может быть вы написали со строчной буквы?:( Нужно с заглавной! :)'
    else:
        sudgests = tree.search(string)
        sudgests = np.sort(sudgests, axis=0)[::-1].tolist()[:10]
        result = '<br>' + '<h1>' + 'Результат поиска по запросу: ' + '<i>' + string + '</i>' + '</h1>' + '</br>'
        for i in sudgests:
            result += '<big>' '<ul>' + '<li>' + '<b>' + i[0] + '</b>' + ' ' + i[1] + '</li>' + '</ul>' + '</big>'
        return json.dumps(result, ensure_ascii = False)
    

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
    return 'Hello, world!'

if __name__ == "__main__":
    app.run()
