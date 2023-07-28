from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import OPE_User
from app import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('inputUsername')
        password = request.form.get('inputPassword')

        user = OPE_User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                flash('Giriş Başarılı!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Şifre Hatalı!', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Giriş Başarısız!', category='error')
            return redirect(url_for('auth.login'))

    else:
        return render_template('account.html', user=current_user)


@auth.route('/register', methods = ['POST'])
def register():
    username = request.form.get('inputUsernameNew')
    password = request.form.get('inputPasswordNew')
    
    if len(username) > 20 or len(username) < 3:
        flash('Kullanıcı adı 3 ile 20 karakter uzunluğunda olmalıdır!', category='error')
        return redirect(url_for('views.account'))

    elif len(password) > 20 or len(password) < 3:
        flash('Şifreniz 3 ile 20 karakter uzunluğunda olmalıdır!', category='error')
        return redirect(url_for('views.account'))

    elif not OPE_User.query.filter_by(username = username).first():
        new_user = OPE_User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt Olundu!', category='success')
        login_user(new_user, remember=True)
        return redirect(url_for('views.home'))
    else:
        flash('Bu Kullanıcı Adı Mevcut!', category='error')
        return redirect(url_for('views.account'))


@auth.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))
