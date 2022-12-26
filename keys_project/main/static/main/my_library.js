const divBookList = document.querySelector('.book-list')
const newBookDiv = document.querySelector('.new-book')
const newBookInput = document.querySelector('.new-book-input')
const newBookBtnAdd = document.querySelector('.new-book-btn-add')
const newBookBtnCancel = document.querySelector('.new-book-btn-cancel')

const bookDiv = document.querySelector('.book')
const bookNameHeader = document.querySelector('.book-name')
const bookDelBtn = document.querySelector('.book-btn-delete')
const bookYesDelBtn = document.querySelector('.book-btn-yes-delete')
let currentBookId

const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const data = JSON.parse(document.getElementById('data').textContent)
let books = {}
// console.log(data)
const waitMs = 1000

onInit()

function onInit() {
    booksSectionConstruct()
    newBookBtnAdd.addEventListener("click", () => { addNewBookBtnClicked() })
    newBookBtnCancel.addEventListener("click", () => { newBookDiv.classList.toggle('hidden') })
    bookDelBtn.addEventListener("click", () => { bookYesDelBtn.classList.remove('hidden') })
    bookYesDelBtn.addEventListener("click", () => { yesDeleteBookClicked() })
}

function booksSectionConstruct() {
    for (let i=0; i<data.length; i++) {
        addBookToList(data[i][0], data[i][1])
        books[data[i][0]] = data[i][1]
    }
    addNewBookBtn()
    // console.log(books)
}

function addBookToList(id, name) {
    const divBookCont = document.createElement('DIV')
    const divBook = document.createElement('DIV')
    divBookCont.classList.add('book-cont')
    divBookCont.classList.add('hoverable')
    divBookCont.setAttribute('id', 'book' + id)
    divBook.classList.add('book-name')
    divBook.textContent = `${name}`
    divBookCont.appendChild(divBook)
    divBookList.appendChild(divBookCont)

    divBookCont.addEventListener("click", (event) => { bookBtnClicked(event.target) })
}

function addNewBookBtn() {
    const divAddBookCont = document.createElement('DIV')
    const divBook = document.createElement('DIV')
    divAddBookCont.classList.add('book-cont')
    divAddBookCont.classList.add('book-cont-add')
    divAddBookCont.classList.add('hoverable')
    divAddBookCont.setAttribute('id', 'new')
    divBook.classList.add('book-plus')
    divBook.textContent = '+'
    divAddBookCont.appendChild(divBook)
    divBookList.appendChild(divAddBookCont)

    divAddBookCont.addEventListener("click", () => {
        // bookYesDelBtn.classList.add('hidden')
        newBookDiv.classList.toggle('hidden')
        // newBookDiv.classList.add('hidden')
        bookDiv.classList.add('hidden')
    });
}

function bookBtnClicked(target) {
    // console.log(target)
    let bookId = parseInt(target.getAttribute('id').replace('book', ''))
    currentBookId = bookId
    // console.log(books[bookId])
    bookYesDelBtn.classList.add('hidden')
    newBookDiv.classList.add('hidden')
    bookDiv.classList.remove('hidden')
    bookNameHeader.textContent = books[bookId]
}

async function addNewBookBtnClicked() {
    const bookName = newBookInput.value
    console.log(bookName.length)
    if (bookName.length > 0 && bookName.length < 256) {
        fetch(`/add_book/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'book_name': bookName})
        })
            // .then(response => response.json())
            // .then(result => {
            //     if (result['result'] == 'success') {
            //         console.log('lol, ok')
            //     } else if (result['result'] == 'failure') {
            //         console.log('lol, not ok')
            //     }
            // })
            // .then(await sleep(waitMs))
            .then(() => { window.location.reload() })
    } else {
        console.log('Invalid name')
    }
}

async function yesDeleteBookClicked() {
    if (currentBookId) {
        fetch(`/delete_book/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'book_id': currentBookId})
        })
            // .then(response => response.json())
            // .then(result => {
            //     if (result['result'] == 'success') {
            //         console.log('lol, ok')
            //     } else if (result['result'] == 'failure') {
            //         console.log('lol, not ok')
            //     }
            // })
            // .then(await sleep(waitMs))
            .then(() => { window.location.reload() })
    } else {
        console.log('no book id')
    }
}

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}
