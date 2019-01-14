from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# Simulates database note in database would not need to asgin college_id
williams = {'image_filename': 'williams_college.jpg', 'location': '880 Main St. Williamstown, MA 01267', 'phone_number':'(413) 597-3131','college_type':'Liberal Arts College','notes':'Your thoughts here','college_id':'1','region':'Northeast','name':'Williams College'}

colleges = [{'image_filename': 'williams_college.jpg', 'location': '880 Main St. Williamstown, MA 01267', 'phone_number':'(413) 597-3131','college_type':'Liberal Arts College','notes':'Your thoughts here','college_id':'1','region':'Northeast','name':'Williams College'},
            {'image_filename':'usc_college.jpg', 'location':'Los Angeles, CA 90007','phone_number':'(213) 740-2311','college_type':'Private University','notes':'Your thoughts here','college_id':'2','region':'West','name':'University of Southern California'},
            {'image_filename':'uni_iowa.jpg','location':'Iowa City, IA 52242','phone_number':'(319) 335-3500','college_type':'Public Research University','notes':'Your thoughts here','college_id':'3','region':'Midwest','name':'University of Iowa'},
            {'image_filename':'uni_montana.jpg','location':' 32 Campus Dr, Missoula, MT 59812','phone_number':'(406) 243-0211','college_type':'Public Research University','notes':'Your thoughts here','college_id':'4','region':'West','name':'University of Montana'}]

regions = ['West', 'Midwest', 'Northeast']


#show all regions
@app.route('/')
@app.route('/region/')
def showRegions():
    return render_template('availableregions.html', colleges=colleges, regions=regions)

#show all colleges for region
@app.route('/region/<region>/')
def showRegionColleges(region):
    return render_template('regionalcolleges.html', colleges=colleges, region=region)

# create new college in same region by clicking link on page that shows all colleges for region
@app.route('/region/<region>/new/')
def addNewCollege(region):
    return render_template('addregionalcollege.html', region=region, colleges=colleges)

# show college by clicking link on page that shows all colleges for region
@app.route('/region/<region>/<int:college_id>/')
def showMyCollege(region, college_id):
    # will filter through for cillege that matches id
    return render_template('mycollege.html', college=williams, colleges=colleges, region=region)

# may go to another page to edit any of college info provided
@app.route('/region/<region>/<int:college_id>/edit')
def editMyCollege(region, college_id):
    return render_template('editregionalcollege.html',region=region,college_id=college_id, item=williams)

# this page allows user to delete colleges
@app.route('/region/<region>/<int:college_id>/delete/')
def deleteMyCollege(region, college_id):
    return render_template('deletemycollege.html',region=region,college_id=college_id, item=williams)


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
