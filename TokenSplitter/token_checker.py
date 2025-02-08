def extract_tokens(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # 各行をコロンで分割し、最後の要素（TOKEN）を取得
            token = line.strip().split(':')[-1]
            # TOKENをresult_alt.txtに書き込む
            outfile.write(token + '\n')

# ファイル名を指定して関数を呼び出す
extract_tokens('alt.txt', 'result_alt.txt')

