import os
app = Flask(__name__)
# downloaded pictures go to static folder
UPLOAD_FOLDER = os.path.basename('static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from database_setup import College, Region, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create session and connect to DB ##
engine = create_engine('sqlite:///colleges.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#show all regions
@app.route('/')
@app.route('/region/')
def showRegions():
    regions = session.query(Region).all()
    return render_template('availableregions.html', regions=regions)

#show all colleges for region
@app.route('/region/<region>/')
def showRegionColleges(region):
    regions = session.query(Region).all()
    # get id of region (not provided in url for simple url)
    region_info = session.query(Region).filter_by(name=region).one()
    # filter id
    regioncolleges = session.query(College).filter_by(college_region_id=region_info.id)
    return render_template('regionalcolleges.html', colleges=regioncolleges, region=region, regions=regions)

# create new college in same region by clicking link on page that shows all colleges for region
@app.route('/region/<region>/new/', methods=['GET','POST'])
# region is a string not an object!
def addNewCollege(region):
    regions = session.query(Region).all()
    if request.method == 'POST':
        file = request.files['image']
        f= os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        file_n = file.filename
        this_region = session.query(Region).filter_by(name=region).one()
        newCollege = College(name = request.form['college_name'], college_region=this_region, location = request.form['location'], phone_number = request.form['phone_number'], college_type = request.form['college_type'], notes = request.form['client_notes'], image_filename=file_n)
        session.add(newCollege)
        session.commit()
        return redirect(url_for('showRegionColleges', region=region, regions=regions))
    else:
        return render_template('addregionalcollege.html', region=region, regions=regions)

# show college by clicking link on page that shows all colleges for region
@app.route('/region/<region>/<int:college_id>/')
def showMyCollege(region, college_id):
    # get region colleges to provide for render template
    regions = session.query(Region).all()
    region_info = session.query(Region).filter_by(name=region).one()
    regioncolleges = session.query(College).filter_by(college_region_id=region_info.id)

    # get college to view
    college = session.query(College).filter_by(college_id=college_id).one()
    return render_template('mycollege.html', college=college, colleges=regioncolleges, region=region, regions=regions, image=college.image_filename)

# may go to another page to edit any of college info provided
@app.route('/region/<region>/<int:college_id>/edit/', methods=['GET','POST'])
def editMyCollege(region, college_id):
    editedItem = session.query(College).filter_by(college_id=college_id).one()
    regions = session.query(Region).all()
    if request.method == 'POST':
        # change college_name  phone_number college_type client_notes
        if request.form['college_name']:
            editedItem.name = request.form['college_name']
        # change location
        if request.form['location']:
            editedItem.location = request.form['location']
        # change phone_number
        if request.form['phone_number']:
            editedItem.phone_number = request.form['phone_number']
        # change college_type
        if request.form['college_type']:
            editedItem.college_type = request.form['college_type']
        # change client_notes
        if request.form['client_notes']:
            editedItem.notes = request.form['client_notes']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMyCollege', region=region, regions=regions, college_id=college_id))
    else:
        return render_template('editregionalcollege.html',region=region, regions=regions, college_id=college_id, item=editedItem)

# this page allows user to delete colleges
@app.route('/region/<region>/<int:college_id>/delete/', methods=['GET','POST'])
def deleteMyCollege(region, college_id):
    itemToDelete = session.query(College).filter_by(college_id=college_id).one()
    regions = session.query(Region).all()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showRegionColleges', region=region, regions=regions))
    else:
        # if get request (including going to the website)
        return render_template('deletemycollege.html', region=region, item=itemToDelete, regions=regions)


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
