#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit(): # 整数部分を読み取る
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.': # 小数点がある場合
        index += 1
        decimal = 0.1 # 小数点以下の値を計算するための変数
        while index < len(line) and line[index].isdigit(): 
            number += int(line[index]) * decimal 
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number} 
    return token, index


def read_plus(line, index): # '+'を読み取る関数
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index): # '-'を読み取る関数
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index): # '*'を読み取る関数
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index): # '/'を読み取る関数
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_leftparenthesis(line, index): # '('を読み取る関数
    token = {'type': 'LEFTPARENTHESIS'}
    return token, index + 1

def read_rightparenthesis(line, index): # ')'を読み取る関数
    token = {'type': 'RIGHTPARENTHESIS'}
    return token, index + 1

def read_abs(line, index): # 'abs'を読み取る関数
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index): # 整数を読み取る関数
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index): # 'round'(四捨五入)を読み取る関数
    token = {'type': 'ROUND'}
    return token, index + 5

def tokenize(line): # トークン化するための関数
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index) # 数字を読み取る
        elif line[index] == '+':
            (token, index) = read_plus(line, index) # '+'を読み取る
        elif line[index] == '-':
            (token, index) = read_minus(line, index) # '-'を読み取る
        elif line[index] == '*':
            (token, index) = read_mul(line, index) # '*'を読み取る
        elif line[index] == '/':
            (token, index) = read_divide(line, index) # '/'を読み取る
        elif line[index] == '(':
            (token, index) = read_leftparenthesis(line, index) # '('を読み取る
        elif line[index] == ')':
            (token, index) = read_rightparenthesis(line, index) # ')'を読み取る
        elif line[index:index+3] == 'abs':
            (token, index) = read_abs(line, index) # 'abs'を読み取る
        elif line[index:index+3] == 'int':
            (token, index) = read_int(line, index) # 'int'を読み取る
        elif line[index:index+5] == 'round':
            (token, index) = read_round(line, index) # 'round'を読み取る
        elif line[index] == ' ': # スペースは無視する
            index += 1
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_plusminus(tokens): # 足し算と引き算を評価する関数
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate_muldiv(tokens): # 掛け算と割り算を評価する関数
    new_tokens = [] # 新しいトークンリストを作成
    index = 0
    while index < len(tokens): # トークンを一つずつ処理
        if tokens[index]['type'] == 'NUMBER': # 数字の場合はそのまま追加
            new_tokens.append(tokens[index])
        elif tokens[index]['type'] == 'MULTIPLY': # *を読み取った場合
            if index + 1 < len(tokens) and tokens[index + 1]['type'] == 'NUMBER':  # 次のトークンが数字の場合
                last_number = new_tokens.pop() # new_tokenに最後に追加した数字をlast_numberに格納
                new_tokens.append({'type': 'NUMBER', 'number': last_number['number'] * tokens[index + 1]['number']}) # 掛け算を行ってnew_tokenに追加
                index += 1
            else:
                print('Invalid syntax after *') # エラー処理
                exit(1)
        elif tokens[index]['type'] == 'DIVIDE': # /を読み取った場合
            if index + 1 < len(tokens) and tokens[index + 1]['type'] == 'NUMBER': # 次のトークンが数字の場合
                last_number = new_tokens.pop() # new_tokenに最後に追加した数字をlast_numberに格納
                if tokens[index + 1]['number'] == 0: # ゼロで割っている場合
                    print('Division by zero error')
                    exit(1)
                new_tokens.append({'type': 'NUMBER', 'number': last_number['number'] / tokens[index + 1]['number']}) # 割り算を行ってnew_tokenに追加
                index += 1
            else:
                print('Invalid syntax after /') # エラー処理
                exit(1)
        else:
            new_tokens.append(tokens[index]) # その他のトークンはそのまま追加
        index += 1
    return new_tokens

def evaluate_inside_parentheses(tokens, index): # 再帰的に括弧を評価する関数
    depth = 1 # 括弧のネストの深さを管理するための変数
    # global subexpr # グローバル変数subexprを使用
    subexpr = [] # 括弧内の式を保存するリスト
    index += 1
    while index < len(tokens) and depth > 0: # 括弧のネストが終わるまでループ
        if tokens[index]['type'] == 'LEFTPARENTHESIS': # '('を読み取った場合
            depth += 1 # ネストの深さを増やす
        elif tokens[index]['type'] == 'RIGHTPARENTHESIS': # ')'を読み取った場合
            depth -= 1 # ネストの深さを減らす
            if depth == 0: # ネストの深さが0になった場合
                break
        if depth > 0: # ネストの深さが0より大きい場合
            subexpr.append(tokens[index]) # 括弧内のトークンを保存
        index += 1
    if depth != 0: # ネストの深さが0にならなかった場合
        print('Mismatched parentheses')
        exit(1)
    value = evaluate(subexpr) # 括弧内の式を再帰的に評価する
    return value, index # 評価結果を返す

def evaluate_parentheses(tokens): # 括弧を含む式を評価する関数
    new_tokens = [] # 新しいトークンリストを作成
    index = 0
    while index < len(tokens): # トークンを一つずつ処理
        if tokens[index]['type'] == 'LEFTPARENTHESIS': # '('を読み取った場合
            value, index = evaluate_inside_parentheses(tokens, index) # 括弧内の式を評価
            new_tokens.append({'type': 'NUMBER', 'number': value}) # 評価結果を新しいトークンリストに追加
        else:
            new_tokens.append(tokens[index]) # その他のトークンはそのまま追加
        index += 1
    return new_tokens 

def evaluate_abs(tokens): # 絶対値を評価する関数
    new_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] != 'ABS': # 'abs'ではないものを読み取った場合
            new_tokens.append(tokens[index]) # その他のトークンはそのまま追加
            index += 1
            continue
        if index + 1 >= len(tokens): # 'abs'の後にトークンがない場合
            break
        
        index += 1
        if tokens[index]['type'] != 'LEFTPARENTHESIS': # '('ではないものが続く場合
            print('Invalid syntax after abs')
            exit(1)

        value, index = evaluate_inside_parentheses(tokens, index) # 括弧内の式を評価
        new_tokens.append({'type': 'NUMBER', 'number': abs(value)}) # 絶対値を計算して追加
        index += 1
    return new_tokens

def evaluate_int(tokens): # 整数化を評価する関数
    new_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] != 'INT': # 'int'ではないものを読み取った場合
            new_tokens.append(tokens[index]) # その他のトークンはそのまま追加
            index += 1
            continue
        if index + 1 >= len(tokens): # 'int'の後にトークンがない場合
            break
        
        index += 1
        if tokens[index]['type'] != 'LEFTPARENTHESIS': # '('ではないものが続く場合
            print('Invalid syntax after int')
            exit(1)

        value, index = evaluate_inside_parentheses(tokens, index) # 括弧内の式を評価
        new_tokens.append({'type': 'NUMBER', 'number': int(value)}) # 絶対値を計算して追加
        index += 1
    return new_tokens

def evaluate_round(tokens): # 四捨五入を評価する関数
    new_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] != 'ROUND': # 'round'ではないものを読み取った場合
            new_tokens.append(tokens[index]) # その他のトークンはそのまま追加
            index += 1
            continue
        if index + 1 >= len(tokens): # 'round'の後にトークンがない場合
            break
        
        index += 1
        if tokens[index]['type'] != 'LEFTPARENTHESIS': # '('ではないものが続く場合
            print('Invalid syntax after round')
            exit(1)

        value, index = evaluate_inside_parentheses(tokens, index) # 括弧内の式を評価
        new_tokens.append({'type': 'NUMBER', 'number': round(value)}) # 絶対値を計算して追加
        index += 1
    return new_tokens

def evaluate(tokens):
    tokens = evaluate_abs(tokens) # 絶対値を評価
    tokens = evaluate_int(tokens) # 整数化を評価
    tokens = evaluate_round(tokens) # 四捨五入を評価
    tokens = evaluate_parentheses(tokens) # 括弧を含む式を評価
    tokens = evaluate_muldiv(tokens) # 掛け算と割り算を評価
    answer = evaluate_plusminus(tokens) # 足し算と引き算を評価
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.0")
    test("1+2*3")
    test("(1+2)*3")
    test("10/2+7")
    test("abs(-10)")
    test("abs(-(2+3))")
    test("int(3.7)")
    test("int(1.1+2.9)")
    test("round(3.5)")
    test("round(2.4+0.6)")
    test("round(abs(-3.6))")
    test("abs(round(-3.6))")
    test("int(round(3.7+0.1))")
    test("abs(int(round(-1.9+0.9)))")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)