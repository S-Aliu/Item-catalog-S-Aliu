from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

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
    # get id of region (not provided in url for simple url)
    region_info = session.query(Region).filter_by(name=region).one()
    # filter id
    regioncolleges = session.query(College).filter_by(college_region_id=region_info.id)
    return render_template('regionalcolleges.html', colleges=regioncolleges, region=region)

# create new college in same region by clicking link on page that shows all colleges for region
@app.route('/region/<region>/new/', methods=['GET','POST'])
def addNewCollege(region):
    if request.method == 'POST':
        newCollege = College(name = request.form['college_name'], college_region=region, location = request.form['location'], phone_number = request.form['phone_number'], college_type = request.form['college_type'], notes = request.form['client_notes'])
        session.add(newCollege)
        session.commit()
        # return render_template('regionalcolleges.html', colleges=colleges, region=region)
        redirect(url_for('showRegionColleges',region=region))
    else:
        return render_template('addregionalcollege.html', region=region)

# show college by clicking link on page that shows all colleges for region
@app.route('/region/<region>/<int:college_id>/')
def showMyCollege(region, college_id):
    # get region colleges to provide for render template
    region_info = session.query(Region).filter_by(name=region).one()
    regioncolleges = session.query(College).filter_by(college_region_id=region_info.id)

    # get college to view
    college = session.query(College).filter_by(college_id=college_id).one()
    return render_template('mycollege.html', college=college, colleges=regioncolleges, region=region, image=college.image_filename)

# may go to another page to edit any of college info provided
@app.route('/region/<region>/<int:college_id>/edit/', methods=['GET','POST'])
def editMyCollege(region, college_id):
    editedItem = session.query(College).filter_by(college_id=college_id).one()
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
        return redirect(url_for('showMyCollege', region=region, college_id=college_id))
    else:
        return render_template('editregionalcollege.html',region=region, college_id=college_id, item=editedItem)

# this page allows user to delete colleges
@app.route('/region/<region>/<int:college_id>/delete/')
def deleteMyCollege(region, college_id):
    itemToDelete = session.query(College).filter_by(college_id=college_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMyCollege', region=region, college_id=college_id))
    else:
        # if get request
        return render_template('deletemycollege.html',region=region,college_id=college_id, item=itemToDelete)


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
