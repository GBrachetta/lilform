from flask import render_template, url_for, flash, redirect
from lilform import app
from lilform.forms import RegistrationForm, LoginForm
from lilform.models import User, Builder, Instrument

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


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'brachetta@me.com' and form.password.data == 'Cuperino68':
            flash('You are logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please check your credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/builders')
def builders():
    return render_template('builders.html', title='Builders')


@app.route('/instruments')
def instrument():
    return render_template('instruments.html', instruments=instruments, title='Instruments')


@app.route('/contributors')
def contributors():
    return render_template('contributors.html')
