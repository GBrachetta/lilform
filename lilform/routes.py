from flask import render_template, url_for, flash, redirect, request
from lilform import app, db, bcrypt
from lilform.forms import RegistrationForm, LoginForm, UpdateAccountForm
from lilform.models import User, Builder, Instrument
from flask_login import login_user, current_user, logout_user, login_required


instruments = [
    {
        'contributor': 'Guillermo Brachetta',
        'instrument_maker': 'Vaudry',
        'location': 'Amsterdam',
        'date_added': '24 April 2020',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam congue mi eget risus elementum malesuada. Donec ut erat a libero molestie gravida. Sed eu tempor ex. Vivamus iaculis lorem sed pretium ultrices. Mauris malesuada velit sit amet quam feugiat, vitae posuere urna condimentum. Proin lacinia eros augue, a euismod lorem finibus et. Duis ullamcorper tellus mauris, sit amet consequat neque efficitur vel. Donec euismod mauris leo, varius pharetra nunc consectetur sed. Donec ultricies lorem dui, et posuere lorem vehicula id. Aliquam erat urna, imperdiet molestie arcu at, tincidunt porttitor enim. Mauris scelerisque finibus magna, vel scelerisque neque pharetra sed. Suspendisse pretium dui ut risus ornare, at faucibus lacus efficitur. In eleifend nibh sed turpis consectetur condimentum.'
    },
    {
        'contributor': 'Menno van Delft',
        'instrument_maker': 'Ruckers',
        'location': 'Paris',
        'date_added': '24 May 2019',
        'description': 'Sed placerat ornare lorem sed egestas. Maecenas eget placerat mi. Curabitur lobortis sagittis elit, lacinia pretium leo iaculis sit amet. Maecenas erat lorem, egestas sit amet odio quis, pretium vehicula libero. Sed accumsan nibh sapien, semper rutrum neque tempus a. Nam gravida, libero eu convallis euismod, enim metus efficitur lectus, at dapibus leo tellus a sapien. Suspendisse porttitor quam lacus, at placerat turpis auctor id. Quisque rutrum, ex a vestibulum volutpat, elit purus ultrices nunc, et porttitor dolor dolor sit amet risus. Vestibulum tempus, felis eget tempor viverra, purus turpis cursus tortor, nec imperdiet justo odio et mauris.'
    },
    {
        'contributor': 'Guillermo Brachetta',
        'instrument_maker': 'Lefebvre',
        'location': 'Paris',
        'date_added': '2 April 2019',
        'description': 'Pellentesque placerat elit eget mi porttitor pretium. In imperdiet molestie massa, at pretium lorem tincidunt non. In volutpat sed eros ut congue. Donec pellentesque mauris est, quis mattis erat molestie non. Curabitur nisi augue, malesuada eget pulvinar eget, faucibus sed nisi. Integer euismod eleifend nisl, at hendrerit leo gravida sit amet. Nam laoreet blandit sapien vitae vehicula. Nullam rhoncus, lacus non tincidunt efficitur, libero purus vulputate odio, non volutpat tellus lacus at odio.'
    }
]

builders = [
    {
        'contributor': 'Guillermo Brachetta',
        'name': 'Guillaume Vaudry',
        'date_added': '24 April 1643',
        'biography': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam congue mi eget risus elementum malesuada. Donec ut erat a libero molestie gravida. Sed eu tempor ex. Vivamus iaculis lorem sed pretium ultrices. Mauris malesuada velit sit amet quam feugiat, vitae posuere urna condimentum. Proin lacinia eros augue, a euismod lorem finibus et. Duis ullamcorper tellus mauris, sit amet consequat neque efficitur vel. Donec euismod mauris leo, varius pharetra nunc consectetur sed. Donec ultricies lorem dui, et posuere lorem vehicula id. Aliquam erat urna, imperdiet molestie arcu at, tincidunt porttitor enim. Mauris scelerisque finibus magna, vel scelerisque neque pharetra sed. Suspendisse pretium dui ut risus ornare, at faucibus lacus efficitur. In eleifend nibh sed turpis consectetur condimentum.'
    },
    {
        'contributor': 'Guillermo Brachetta',
        'name': 'Etiénne Lefebvre',
        'date_added': '2 December 1664',
        'biography': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam congue mi eget risus elementum malesuada. Donec ut erat a libero molestie gravida. Sed eu tempor ex. Vivamus iaculis lorem sed pretium ultrices. Mauris malesuada velit sit amet quam feugiat, vitae posuere urna condimentum. Proin lacinia eros augue, a euismod lorem finibus et. Duis ullamcorper tellus mauris, sit amet consequat neque efficitur vel. Donec euismod mauris leo, varius pharetra nunc consectetur sed. Donec ultricies lorem dui, et posuere lorem vehicula id. Aliquam erat urna, imperdiet molestie arcu at, tincidunt porttitor enim. Mauris scelerisque finibus magna, vel scelerisque neque pharetra sed. Suspendisse pretium dui ut risus ornare, at faucibus lacus efficitur. In eleifend nibh sed turpis consectetur condimentum.'
    },
    {
        'contributor': 'Guillermo Brachetta',
        'name': 'Hans Ruckers',
        'date_added': '24 June 1572',
        'biography': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam congue mi eget risus elementum malesuada. Donec ut erat a libero molestie gravida. Sed eu tempor ex. Vivamus iaculis lorem sed pretium ultrices. Mauris malesuada velit sit amet quam feugiat, vitae posuere urna condimentum. Proin lacinia eros augue, a euismod lorem finibus et. Duis ullamcorper tellus mauris, sit amet consequat neque efficitur vel. Donec euismod mauris leo, varius pharetra nunc consectetur sed. Donec ultricies lorem dui, et posuere lorem vehicula id. Aliquam erat urna, imperdiet molestie arcu at, tincidunt porttitor enim. Mauris scelerisque finibus magna, vel scelerisque neque pharetra sed. Suspendisse pretium dui ut risus ornare, at faucibus lacus efficitur. In eleifend nibh sed turpis consectetur condimentum.'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check your credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/builders')
def builder():
    return render_template('builders.html', builders=builders, title='Builders')


@app.route('/instruments')
def instrument():
    return render_template('instruments.html', instruments=instruments, title='Instruments')


@app.route('/contributors')
def contributors():
    return render_template('contributors.html')
