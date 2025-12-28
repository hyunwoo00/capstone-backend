import pandas as pd
# csv바탕으로 init.sql 생성. 
# init.sql은 도커 db 컨테이너 생성시 실행되는 sql파일
# CSV 파일 경로
df = pd.read_csv("yamnet_labels.csv")

with open("init.sql", "w", encoding="utf-8") as f:
    # 테이블 생성 SQL
    f.write("""
CREATE TABLE yamnet_labels (
    id INT PRIMARY KEY,
    mid VARCHAR(50),
    display_name VARCHAR(255),
    display_name_kor VARCHAR(255),
    label_category INT
);\n\n""")

    f.write("INSERT INTO yamnet_labels (id, mid, display_name, display_name_kor, label_category) VALUES\n")

    # INSERT VALUES
    for i, row in df.iterrows():
        idx = int(row['index'])
        mid = row['mid'].replace("'", "''")
        name = row['display_name'].replace("'", "''")
        kor = row['display_name_kor'].replace("'", "''")
        cat = int(row['label_category'])

        line = f"({idx}, '{mid}', '{name}', '{kor}', {cat})"
        f.write(line)
        f.write(",\n" if i < len(df) - 1 else ";\n")
