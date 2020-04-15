from flask_restful import Resource, Api
from flask import Flask, Response, json, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/mhs'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


# Ini adalah materi Pertemuan 3
@app.route('/')
def hello_world():
    return 'Selamat Datang'

@app.route('/admin')
def admin_page():
    return 'Ini adalah Halaman Admin'

# Materi Pertemuan 3 berakhir disini


# Ini adalah materi Pertemuan 4
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/helloworld')

# Materi Pertemuan 4 berakhir disini

# Ini adalah materi Pertemuan 5

#class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(80), unique=True)
#  email = db.Column(db.String(120), unique=True)

#    def __init__(self, username, email):
#       self.username = username
#       self.email = email


#    @staticmethod
#    def get_all_users():
#      return User.query.all()


#class UserSchema(ma.Schema):
#    class Meta:
        # Fields to expose
#        fields = ('username', 'email')


#user_schema = UserSchema()
#users_schema = UserSchema(many=True)


#@app.route("/user/", methods=["GET"])
#def get_user():
#    all_users = User.get_all_users()
#    result = users_schema.dump(all_users)
#    return jsonify(result)

# Materi Pertemuan 5 berakhir disini

# ini adalah Tugas Pertemuan 6
class Mhs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True)
    nama = db.Column(db.String(50))
    kelas = db.Column(db.String(10))
    alamat= db.Column(db.String(100))

    def __init__(self, nim, nama, kelas, alamat):
        self.nim = nim
        self.nama = nama
        self.kelas = kelas
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mhs.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'nama', 'kelas', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/mahasiswa', methods=['POST'])
def add_user():
    nim = request.json['nim']
    nama = request.json['nama']
    kelas = request.json['kelas']
    alamat = request.json['alamat']

    new_mhs = Mhs(nim, nama, kelas, alamat)

    db.session.add(new_mhs)
    db.session.commit()

    return user_schema.jsonify(new_mhs)

@app.route('/mahasiswa', methods=['GET'])
def get_users():
    all_users = Mhs.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/mahasiswa/<int:id>', methods=['GET'])
def get_user(id):
  mahasiswa = Mhs.query.get(id)
  return user_schema.jsonify(mahasiswa)

@app.route('/user/<int:id>', methods=['POST'])
def create_user(id):
    mahasiswa = Mhs.query.get(id)

    nim = request.json['nim']
    nama = request.json['nama']
    kelas = request.json['kelas']
    alamat = request.json['alamat']

    mahasiswa.nim = nim
    mahasiswa.nama = nama
    mahasiswa.kelas = kelas
    mahasiswa.alamat = alamat

    db.session.add(mahasiswa)
    db.session.commit()

    result = user_schema.dump(mahasiswa)
    return jsonify(result)

@app.route('/mahasiswa/<int:id>', methods=['PUT'])
def update_user(id):
  mahasiswa = Mhs.query.get(id)

  nim = request.json['nim']
  nama = request.json['nama']
  kelas = request.json['kelas']
  alamat = request.json['alamat']

  mahasiswa.nim = nim
  mahasiswa.nama = nama
  mahasiswa.kelas = kelas
  mahasiswa.alamat = alamat

  db.session.commit()
  result = user_schema.dump(mahasiswa)
  return jsonify(result)

@app.route('/mahasiswa/<int:id>', methods=['DELETE'])
def delete_product(id):
  mahasiswa = Mhs.query.get(id)
  db.session.delete(mahasiswa)
  db.session.commit()

  return jsonify()
# Tugas Pertemuan 6 berakhir disini

if __name__ == '__main__':
    app.run()
