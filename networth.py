from reactpy import component, html, hooks, event, utils
from reactpy.backend.fastapi import configure, Options
from fastapi import FastAPI
from sqlmodeldb import (create_db_and_tables, add_deal,
                        select_deals, delete_deal)
import pandas as pd


create_db_and_tables()


BOOTSTRAP_CSS = html.link(
    {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/'
                'dist/css/bootstrap.min.css',
        'integrity': 'sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Y'
                     'z1ztcQTwFspd3yD65VohhpuuCOmLASjC',
        'crossorigin': 'anonymous',
    }
)

PAGE_HEADER_TITLE = 'ReactPy-NetWorth'


CARD_TEXT_COLOR = {'Assets': 'text-success', 'Liabilities': 'text-danger',
                   'Net Worth': 'text-primary'}


CAT_OPTIONS = ['Clothing', 'Donation', 'Education', 'Food', 'Healthcare',
               'Housing', 'Income', 'Insurance', 'Loans', 'Others',
               'Personals', 'Recreation', 'Retirement', 'Supplies',
               'Transportation', 'Utilities']


def get_records(db) -> list[list]:
    """Converts db to list of list.
    
    Args:
        db: A list of Deal class from sqlmodeldb module.
    """
    return [[da.id, da.date, da.value, da.category, da.comment] for da in db]


def select_options():
    return [html.option(opt) for opt in CAT_OPTIONS]


@component
def FormDateInput(date, set_date):
    return html.div(
        {'class': 'mb-3'},
        html.label(
            {
                'class': 'form-label fw-bold',
                'for': 'date'
            },
            'Date',
        ),
        html.input(
            {
                'class': 'form-control',
                'type': 'date',
                'id': 'date',
                'placeholder': 'enter date',
                'on_change': lambda event: set_date(event['target']['value']),
                'value': date,
            },
        ),
    )


@component
def FormAmountInput(amount, set_amount):
    return html.div(
        {'class': 'mb-3'},
        html.label(
            {
                'class': 'form-label fw-bold',
                'for': 'amount'
            },
            'Amount',
        ),
        html.input(
            {
                'class': 'form-control',
                'type': 'text',
                'id': 'amount',
                'placeholder': 'enter amount',
                'on_change': lambda event: set_amount(event['target']['value']),
                'value': amount,
            },
        ),
    )


@component
def FormSelect(category, set_category):
    return html.div(
        {'class': 'mb-3'},
        html.label(
            {
                'class': 'form-label fw-bold',
                'for': 'category'
            },
            'Category',
        ),
        html.select(
            {
                'class': 'form-select',
                'id': 'category',
                'on_change': lambda event: set_category(event['target']['value']),
                'value': category,
            },
            select_options(),
        ),
    )


@component
def FormCommentInput(comment, set_comment):
    return html.div(
        {'class': 'mb-3'},
        html.label(
            {
                'class': 'form-label fw-bold',
                'for': 'comment',
            },
            'Comment',
        ),
        html.input(
            {
                'class': 'form-control',
                'type': 'text',
                'id': 'comment',
                'placeholder': 'enter comment',
                'on_change': lambda event: set_comment(event['target']['value']),
                'value': comment,
            },
        ),
    )


@component
def FormSaveButton():
    return html.input(
        {
            'class': 'btn btn-primary mb-3',
            'type': 'submit',
            'value': 'Save'
        },
    )


@component
def FormDeleteInput(bad_id, set_bad_id):
    return html.div(
        {'class': 'mt-3'},
        html.label(
            {
                'class': 'form-label fw-bold',
                'for': 'bad_id'
            },
            'Id to delete',
        ),
        html.input(
            {
                'class': 'form-control',
                'type': 'text',
                'id': 'bad_id',
                'placeholder': 'enter id to delete',
                'on_change': lambda event: set_bad_id(event['target']['value']),
                'value': bad_id
            },
        ),
    )


@component
def FormDeleteButton():
    return html.input(
        {
            'class': 'btn btn-danger my-3',
            'type': 'submit',
            'value': 'Delete',
        }
    )


@component
def Card(label, amount):
    """Shows label and amount in a bootstrap card.
    
    Text color is styled depending on the label and amount.
    """
    text_color = CARD_TEXT_COLOR[label]
    if label == 'Net Worth' and amount < 0:
        text_color = 'text-warning'
    return html.div(
        {'class': 'col-sm-4'},
        html.div(
            {'class': 'card mb-3 border-primary'},
            html.div(
                {'class': 'card-body'},
                html.div(
                    {'class': f'card-title {text_color}'},
                    html.h5(
                        {'style': {'font-family': 'Chalkduster, fantasy'}},
                        label
                    ),
                ),
                html.div(
                    {'class': 'card-text'},
                    html.span({'class': f'{text_color} fw-bold'}, amount),
                ),
            ),
        ),
    )


@component
def Summary():
    """Generates three cards for asset, liability and net worth.

    These cards are displayed in a row at the top of the page.    
    The asset and liablity values are taken from the sqlite database
    using SQLModel library.

    All positive amounts are assets whereas all negative
    amounts are liabilities.
    """
    db_results = select_deals()
    records = get_records(db_results)

    asset_value = sum([rec[2] for rec in records if rec[2] >= 0])
    liability_value = sum([rec[2] for rec in records if rec[2] < 0])
    net_value = asset_value + liability_value

    return html.div(
        html.div(
            {'class': 'row'},
            Card('Assets', asset_value),
            Card('Liabilities', liability_value),
            Card('Net Worth', net_value),
        ),
    )


@component
def DealHistory():
    """Displays the history of deals or transactions.

    Converts sqlite records to dataframe using pandas then to html and
    finally to vdom.
    """
    db_results = select_deals()
    records = get_records(db_results)

    # Show records in reverse order or latest deals first.
    records = records[::-1]

    df = pd.DataFrame(
        records,
        columns=['Id', 'Date', 'Amount', 'Category', 'Comment']
    )
    html_rec = df.to_html(
        index=False,
        border=0,
        justify='center',
        classes=[
            'table', 'table-primary',
            'table-bordered', 'text-center',
            'table-striped', 'table-hover'
        ]
    )
    return html.div(
        html.div({'class': 'fw-bold'}, 'Deals history'),
        html.div(
            {
                'class': 'mt-2',
                'style': {
                    'height': '210px',
                    'overflow-y': 'auto',
                }
            },
            utils.html_to_vdom(html_rec),
        ),
    )


@component
def NetWorth():
    date, set_date = hooks.use_state('')
    amount, set_amount = hooks.use_state('')
    category, set_category = hooks.use_state('')
    comment, set_comment = hooks.use_state('')
    bad_id, set_bad_id = hooks.use_state('')

    @event(prevent_default=True)
    def delete_id(event):
        delete_deal(int(bad_id))
        set_bad_id('')

    @event(prevent_default=True)
    def save_record(event):
        if amount == '':
            return
        add_deal(date, amount, category, comment)

        # Reset
        set_date('')
        set_amount('')
        set_category('')
        set_comment('')

    return html.div(
        BOOTSTRAP_CSS,
        html.div(
            {'class': 'container mt-3'},
            Summary(),
            html.div(
                {'class': 'row'},
                html.div(
                    {'class': 'col-lg-6'},
                    html.form(
                        {'on_submit': save_record},
                        FormDateInput(date, set_date),
                        FormAmountInput(amount, set_amount),
                        FormSelect(category, set_category),
                        FormCommentInput(comment, set_comment),
                        FormSaveButton(),
                    ),
                ),
                html.div(
                    {'class': 'col-lg-6'},
                    DealHistory(),
                    html.form(
                        {'on_submit': delete_id},
                        FormDeleteInput(bad_id, set_bad_id),
                        FormDeleteButton(),
                    ),
                ),
            ),
        ),
    )


app = FastAPI()
configure(
    app,
    NetWorth,
    options=Options(
        head=html.head(
            html.title(PAGE_HEADER_TITLE)
        )
    )
)
