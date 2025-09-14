{
    'name': 'Impresión de tickets desde Inventario - PERUANITA',
    'version': '1.0',
    'summary': 'Impresión de tickets para movimientos de inventario',
    'description': """
        Add button to print ticket for stock pickings
    """,
    'author': 'Juan Salvador',
    'website': 'https://jsalvador.dev',
    'category': 'Inventory',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'peruanita_stock_ticket/static/src/css/ticket.css',
            'peruanita_stock_ticket/static/src/js/picking_ticket.js',
            'peruanita_stock_ticket/static/src/xml/picking_ticket_templates.xml',
        ],
        'web.assets_frontend': [
            'peruanita_stock_ticket/static/src/css/ticket.css',
            'peruanita_stock_ticket/static/src/css/stock_receipts.css'
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'
}