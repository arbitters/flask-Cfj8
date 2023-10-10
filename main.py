from config import TOKEN, CLIENT_SECRET, REDIRECT_URL_LEAGUE,REDIRECT_URL_COUNTER,OAUTH_URL_LEAGUE,OAUTH_URL_COUNTER
from flask import Flask, render_template, request,session
from flask_mysqldb import MySQL
from zenora import APIClient


app = Flask(__name__)

app.secret_key = '1hello2'

app.config['MYSQL_HOST'] = 'containers-us-west-120.railway.app'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0en6pbybktiIE41UpRnu'
app.config['MYSQL_PORT'] = 6415
app.config['MYSQL_DB'] = 'railway'

mysql = MySQL(app)



client = APIClient(TOKEN,client_secret=CLIENT_SECRET)

def create_league_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS league (
            id INT AUTO_INCREMENT PRIMARY KEY,
            discordUser VARCHAR(255) UNIQUE,
            leagueUser VARCHAR(255),
            walletAddress VARCHAR(255),
            leagueServer VARCHAR(255)
        )
    """)
    cur.close()

def create_counter_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INT AUTO_INCREMENT PRIMARY KEY,
            discordUser VARCHAR(255) UNIQUE,
            counterUser VARCHAR(255),
            walletAddress VARCHAR(255),
            counterServer VARCHAR(255)
        )
    """)
    cur.close()


@app.before_request
def before_request():
    create_league_table()
    create_counter_table()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/counterPage")
def counter():
    return render_template('counterPage.html', oauth_uri=OAUTH_URL_COUNTER)


@app.route("/leaguePage")
def league():
    return render_template('leaguePage.html', oauth_uri=OAUTH_URL_LEAGUE)


@app.route("/oauth/callback/league")
def callbackLeague():

    try:
        code = request.args['code']
        access_token = client.oauth.get_access_token(code, redirect_uri=REDIRECT_URL_LEAGUE).access_token
        bearer_client = APIClient(access_token, bearer=True)
        current_user = bearer_client.users.get_current_user().username
        session['current_user'] = current_user
        return render_template('league.html')

    except Exception as ex:
        return render_template('invalid.html')


@app.route("/oauth/callback/counter")
def callbackCounter():

    try:
        code = request.args['code']
        access_token = client.oauth.get_access_token(code, redirect_uri=REDIRECT_URL_COUNTER).access_token
        bearer_client = APIClient(access_token, bearer=True)
        current_user = bearer_client.users.get_current_user().username
        session['current_user'] = current_user
        return render_template('counter.html')

    except Exception as ex:
        return render_template('invalid.html')

@app.route('/registerLeague', methods=['POST', 'GET'])
def leagueRegister():

    if request.method == 'POST':
        leagueUser = request.form['leagueUser']
        walletAddress = request.form['walletAddress']
        leagueServer = request.form['leagueServer']
        discordUser = session.get('current_user')
        cur = mysql.connection.cursor()

        cur.execute("SELECT discordUser FROM league WHERE discordUser = %s", (discordUser,))
        existing_user = cur.fetchone()

        if existing_user:
            already_registered = True
            cur.close()
            return render_template('league.html', already_registered=already_registered)

        cur.execute("INSERT INTO league (discordUser, leagueUser, walletAddress, leagueServer) VALUES (%s, %s, %s, %s)",
                    (discordUser, leagueUser, walletAddress, leagueServer))
        mysql.connection.commit()
        cur.close()
        registration_successful = True
        return render_template('league.html', registration_successful=registration_successful)

    return render_template('index.html', already_registered=False)


@app.route('/registerCounter', methods=['POST', 'GET'])
def counterRegister():

    if request.method == 'POST':
        leagueUser = request.form['counterUser']
        walletAddress = request.form['walletAddress']
        counterServer = request.form['counterServer']
        discordUser = session.get('current_user')
        cur = mysql.connection.cursor()

        cur.execute("SELECT discordUser FROM counter WHERE discordUser = %s", (discordUser,))
        existing_user = cur.fetchone()

        if existing_user:
            already_registered = True
            cur.close()
            return render_template('counter.html', already_registered=already_registered)

        cur.execute("INSERT INTO counter (discordUser, counterUser, walletAddress, counterServer) VALUES (%s, %s, %s, %s)",
                    (discordUser, leagueUser, walletAddress, counterServer))
        mysql.connection.commit()
        cur.close()
        registration_successful = True
        return render_template('counter.html', registration_successful=registration_successful)

    return render_template('index.html', already_registered=False)



if __name__ == '__main__':
    app.run(debug=True)


