from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from models import OPE_Episodes, OPE_Contact
from bs4 import BeautifulSoup
from app import db
import requests



views = Blueprint('views', __name__)

@views.route('/')
def home():
    
    epidsode_list = db.session.execute(db.select(OPE_Episodes)).scalars()

    return render_template('index.html', epidsode_list=epidsode_list, user=current_user)


@views.route('/ep_download' , methods=['POST'])
def watch():

    id = request.form.get('episode_id')
    url = (OPE_Episodes.query.filter_by(id=id).first()).url
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    div_element = soup.find('div', id='bolum_indir')
    
    element = div_element.find('a', href=True)
    href_content = 'https://animekalesi.com/' + element['href']

    return redirect(href_content)


@views.route('/account')
def account():
    return render_template('account.html', user=current_user)


@views.route('/about')
def about():
    return render_template('about.html', user=current_user)


@views.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)



@views.route('/refresh')
@login_required
def refresh():
    if current_user.id == 1:
        url = 'https://animekalesi.com/altyazib-115-one-piece.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a')
        
        for a_tag in a_tags:
            title = a_tag.get('title', '')
            href = a_tag.get('href', '')


            if 'one-piece' in href and '. Bölüm Türkçe Altyazısı' in title:
                href = 'https://animekalesi.com/' + href
                title = title.replace(' Altyazısı', '')
                query = OPE_Episodes.query.filter_by(url = href).first()

                if not query:
                    new_episode = OPE_Episodes(url = href, title = title)
                    db.session.add(new_episode)
                    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/watched_ep/<watched_id>')
@login_required
def watched_ep(watched_id):

    current_user.last_episode = watched_id
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/change_setting/<set_id>')
@login_required
def change_setting(set_id):

    current_user.list_setting = int(set_id)
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/send_contact', methods=['GET', 'POST'])
def send_contact():

    message = request.form.get('message_area')
    if current_user.is_authenticated == True:
        new_message = OPE_Contact(user_id=current_user.id, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Geribildirim Gönderildi!', category='success')
    else:
        new_message = OPE_Contact(user_id=0, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Geribildirim Gönderildi!', category='success')

    return redirect(url_for('views.home'))

