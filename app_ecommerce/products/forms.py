from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FloatField,  SelectField
from wtforms.validators import DataRequired,Length
from app_ecommerce.categories.utils import get_categories_allowed

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

class ProductsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2,max=80)])
    description = TextAreaField('Description', validators=[DataRequired(),Length(min=2,max=2500 )])
    weight = StringField('Weight',validators=[DataRequired()])
    price = FloatField('Price(COP)', validators=[DataRequired()])
    image1 = FileField('Insert Image 1',validators=[FileAllowed(['jpg','png'])])
    image2 = FileField('Insert Image 2',validators=[FileAllowed(['jpg', 'png'])])
    image3 = FileField('Insert Image 3',validators=[FileAllowed(['jpg', 'png'])])
    category = NonValidatingSelectField('Category',choices=get_categories_allowed())
    spent = NonValidatingSelectField('Spent?',choices=[ (False, 'False'),(True, 'True') ])

    submit = SubmitField('Create Product')

