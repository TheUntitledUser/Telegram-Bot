import sqlite3

def fetch_records():
    conn = sqlite3.connect('cartridges.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, cabinet, model, replacement_date, date_of_transfer, return_date, counter_before_replacement, counter_after_replacement, number_of_pages FROM cartridge_records')
    records = cursor.fetchall()
    conn.close()
    return records

def generate_table(records):
    rows_html = ""
    for row in records:
        rows_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td></tr>"
    return rows_html

def update_html_file():
    records = fetch_records()
    if not records:
        rows_html = "<tr><td colspan='4'>Нет данных</td></tr>"
    else:
        rows_html = generate_table(records)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Учет картриджей</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Записи о замене картриджей</h1>
        <table>
            <tr>
                <th>Имя пользователя</th>
                <th>Кабинет</th>
                <th>Модель</th>
                <th>Дата замены</th>
                <th>Дата передачи</th>
                <th>Дата возврата</th>
                <th>Счетчик отпечатанных страниц до замены</th>
                <th>Счетчик отпечатанных страниц после замены</th>
                <th>Общее количество отпечатанных страниц</th>
            </tr>
            {rows_html}
        </table>
    </body>
    </html>
    """

    with open("cartridge_records.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == '__main__':
    update_html_file()
