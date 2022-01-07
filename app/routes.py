from app            import app, bcrypt, mail, qrcode, login_manager
from app.models     import db, User, Ressource, Localisation, Ressource, Anomalie

from flask          import render_template, request, jsonify, redirect, url_for, flash
from flask_mail     import Message
from flask_login    import login_required, current_user, login_user, logout_user

from werkzeug.urls  import url_parse

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

########################################################
#                   Authentification                   #
########################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        user = User.query.filter_by( email = request.form.get('email') ).first()
        if user is None :
            flash("L'adresse mail n'existe pas", "danger")
            return redirect(url_for('login'))
        elif not bcrypt.check_password_hash(user.password, request.form.get('password')):
            flash('Le mot de passe est incorrecte', "danger")
            return redirect(url_for('login'))
        login_user(user, remember=request.form.get('remember'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html')

@app.route('/nvMdp', methods=['GET', 'POST'])
def mdp_requet():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        user = User.query.filter_by( email = request.form.get('email') ).first()
        if user is None :
            flash("L'adresse mail n'existe pas", "danger")
        else:
            token = user.get_reini_token()
            msg = Message(
                "Mot de passe",
                sender = "miniprojet.faikahm@gmail.com",
                recipients = [user.email]
            )
            msg.body = f"""Bonjour {user.prenom}
L'adresse mail {user.email} est utilsée pour réinitialiser le mot de passe
Cliquer sur le lien suivant pour la rénitialiser 
{url_for('mdp_reini', token=token, _external=True)}
Si vous n'etiez pas le demandeur veuillez contacter l'admin.

Remarque le lien expirera en 24h
"""
            mail.send(msg)
            flash("Un lien de réinitialisation est envoyé à votre email", "success")
            return redirect(url_for('login'))
    return render_template('motDePasse.html')

@app.route('/nvMdp/<token>', methods=['GET', 'POST'])
def mdp_reini(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verifier_reini_token(token)
    if user is None:
        flash("Le lien est expiré", "danger")
        return redirect(url_for('mdp_requet'))
    elif request.method == 'POST':
        if request.form.get('password') == request.form.get('password_conf'):
            user.password = bcrypt.generate_password_hash(request.form.get('password'), 5)
            db.session.commit()
            flash("Votre mot de passe est bien été réinilialisé", "success")
            return redirect(url_for('login'))
        else:
            flash("Les mots de passe ne correspondent pas", "danger")
            return redirect(url_for('mdp_reini', token=token))
    return render_template('motDePasseReini.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

########################################################
#                   signaler anomalie                  #
########################################################

@app.route('/signaler/<id>')
def lister_anomalies(id):
    ressource = Ressource.query.filter_by(id = int(id)).first()
    page = request.args.get('page', 1, type=int)
    anomalies = Anomalie.query.filter_by(ressource_id = int(ressource.id)).paginate(page=page, per_page=8)
    return render_template("anomalies.html", anomalies=anomalies, ressource=ressource)

@app.route('/signaler/<id>/add', methods = ['GET', 'POST'])
def signaler_anomalie(id):
    ressource = Ressource.query.filter_by(id = int(id)).first()
    localisations = Localisation.query.all()
    if request.method == 'POST':
        anomalie = Anomalie(
            request.form.get('ressource'),
            request.form.get('description')
        )
        db.session.add(anomalie)
        db.session.commit()
        return redirect('/signaler/' + str(id))
    return render_template("anomalie.html", ressource=ressource, localisations=localisations)

@app.route('/signaler/<id>/arr/<ano_id>')
@login_required
def arreter_anomalie(id, ano_id):
    ressource = Ressource.query.filter_by(id = int(id)).first()
    if current_user.get_id() == ressource.responsable_id:
        anomalie = Anomalie.query.filter_by(id = int(ano_id)).first()
        db.session.delete(anomalie)
        db.session.commit()
    return redirect('/signaler/'+ str(id))

@app.route('/ressources/<localisation>')
def api_localisation(localisation):
    ressources = Ressource.query.filter_by(localisation_id = int(localisation)).all()
    ressource_list = []
    for ressource in ressources:
        ressource_dict = {}
        ressource_dict['id'] = ressource.id
        ressource_dict['nom'] = ressource.nom
        ressource_list.append(ressource_dict)
    return jsonify({ 'ressources' : ressource_list })


########################################################
#                   Gerer ressources                   #
########################################################

@app.route('/ressources')
@login_required
def lister_ressources():
    page = request.args.get('page', 1, type=int)
    ressources = Ressource.query.filter_by(responsable_id = int(current_user.get_id())).paginate(page=page, per_page=8)
    localisations = Localisation.query.all()
    localisadicti = { localisation.id : localisation.nom for localisation in localisations }
    return render_template("ressources.html", ressources=ressources, localisations=localisadicti)

@app.route('/ressources/qrcode/<id>')
@login_required
def imprimer_qr(id):
    ressource = Ressource.query.filter_by(id = int(id)).first()
    if int(current_user.get_id()) == int(ressource.responsable_id):
        url = url_for('lister_anomalies', id=id)
        qr_code = qrcode(url)
        return render_template("qrcode.html", qr=qr_code, url=url)
    return redirect(url_for('index'))

@app.route('/ressources/add', methods = ['GET', 'POST'])
@login_required
def ajouter_ressource():
    if request.method == 'POST':
        ressource = Ressource(
            request.form.get('nom'),
            request.form.get('description'),
            current_user.get_id(),
            request.form.get('localisation')
        )
        db.session.add(ressource)
        db.session.commit()
    return redirect(url_for('lister_ressources'))

@app.route('/signaler/<id>/supp')
@login_required
def supprimer_ressource(id):
    ressource = Ressource.query.filter_by(id = int(id)).first()
    db.session.delete(ressource)
    db.session.commit()
    return redirect(url_for('lister_ressources'))


########################################################
#                  Ajouter Localisation                #
########################################################

@app.route('/localisations/add', methods = ['GET', 'POST'])
@login_required
def ajouter_localisation():
    if request.method == 'POST':
        localisation = Localisation(
            request.form.get('nom'),
        )
        db.session.add(localisation)
        db.session.commit()
        return redirect(url_for('lister_ressources'))
    return render_template("localisation.html")


########################################################
#                   Gerer responsables                 #
########################################################

@app.route('/responsables')
@login_required
def lister_responsables():
    if current_user.get_fonct() == 'admin':
        page = request.args.get('page', 1, type=int)
        responsables = User.query.paginate(page=page, per_page=8)
        return render_template("responsables.html", responsables=responsables)
    else:
        return redirect(url_for('lister_ressources'))

@app.route('/responsables', methods = ['GET', 'POST'])
@login_required
def ajouter_responsable():
    if current_user.get_fonct() == 'admin':
        if request.method == 'POST':
            password = 'pass' + request.form.get('nom') + request.form.get('prenom')[:3]
            responsable = User(
                request.form.get('email'),
                bcrypt.generate_password_hash(password, 5),
                request.form.get('nom'),
                request.form.get('prenom'),
                request.form.get('fonction')
            )
            db.session.add(responsable)
            db.session.commit()

            email = request.form.get('email')
            msg = Message(
                "Mot de passe",
                sender = app.config.get("MAIL_USERNAME"),
                recipients = [email]
            )
            msg.html = "<h3>Password</h3><br> \
                        <p> \
                            Bonjour " + request.form.get('prenom') + "<br> \
                            Votre mail est : " + email + "<br> \
                            Voici votre mot de passe: " + password + " \
                        </p>"
            mail.send(msg)
        return redirect(url_for('lister_responsables'))

@app.route('/responsables/<id>/supp')
@login_required
def supprimer_responsable(id):
    if current_user.get_fonct() == 'admin':
        responsable = User.query.filter_by(id = int(id)).first()
        db.session.delete(responsable)
        db.session.commit()
        return redirect(url_for('lister_responsables'))