# -*- coding: utf-8 -*-
{
    'name': "viin_education",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': 2,

    'author': "My Company",
    'website': "http://www.google.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0.',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/education_security.xml',
        'security/ir.model.access.csv',
        'data/education_subject_data.xml',
        'data/education_school_data.xml',
        'data/education_student_stage_data.xml',
        'data/education_teacher_stage_data.xml',
        'views/education_student_views.xml',
        'views/education_student_stage.xml',
        'views/education_student_score_views.xml',
        'views/student_level_views.xml',
        'views/education_subject_views.xml',
        'views/education_class_views.xml',
        'views/education_teacher_views.xml',
        'views/education_school_views.xml',
        
        'views/teacher_level_views.xml',
        'views/education_class_vip.xml',
        'wizards/education_student_note_wizard.xml',
        'wizards/education_student_description_wizard.xml',
        'wizards/education_student_dropout_wizard.xml',
        'wizards/education_teacher_dismissal_wizard.xml',
        'wizards/education_school_group_type_wizard.xml',
        'reports/education_student_information_templates.xml',
        'reports/education_student_information_report.xml',
        'reports/education_student_score_templates.xml',
        'reports/education_student_score_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/education_class_demo.xml',
        'demo/education_teacher_demo.xml',
        'demo/student_level_demo.xml',
        # 'demo/demo.xml',
        # 'demo/demo.xml',
        # 'demo/demo.xml',
        # 'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto-install': False,
    
}
