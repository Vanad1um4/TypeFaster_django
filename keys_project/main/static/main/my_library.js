const divBookList = document.querySelector('.book-list')
const newBookDiv = document.querySelector('.new-book')
const newBookInput = document.querySelector('.new-book-input')
const newBookBtnAdd = document.querySelector('.new-book-btn-add')
const newBookBtnCancel = document.querySelector('.new-book-btn-cancel')

const bookDiv = document.querySelector('.book')
const bookNameHeader = document.querySelector('.book-name')
const bookRenameInput = document.querySelector('.book-rename-input')
const bookRenameBtn = document.querySelector('.book-btn-rename')
const bookDelBtn = document.querySelector('.book-btn-delete')
const bookYesDelBtn = document.querySelector('.book-btn-yes-delete')
let currentBookId

const loadingGif = document.querySelector('.loading')
const textsMainCont = document.querySelector('.texts-cont')

const addTextMainDiv = document.querySelector('.add-text-main-cont')
const addTextPlusDiv = document.querySelector('.add-text-plus')
const addTextInputCont = document.querySelector('.add-text-input-cont')
const addChapterInput = document.querySelector('.add-chapter-input')
const addTextInput = document.querySelector('.add-text-input')

const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const data = JSON.parse(document.getElementById('data').textContent)
let books = {}
console.log(data)
const wain1sec = 1000
const wait3sec = 3000

onInit()

function onInit() {
    booksSectionConstruct()
    newBookBtnAdd.addEventListener("click", () => { addNewBookBtnClicked() })
    newBookBtnCancel.addEventListener("click", () => { newBookDiv.classList.toggle('hidden') })

    bookRenameBtn.addEventListener("click", () => {
        bookRenameInput.classList.toggle('hidden')
        bookNameHeader.classList.toggle('hidden')
    })
    bookRenameInput.addEventListener("input", () => { saveBookNewName() });
    bookDelBtn.addEventListener("click", () => { bookYesDelBtn.classList.remove('hidden') })
    bookYesDelBtn.addEventListener("click", () => { yesDeleteBookClicked() })

    addTextPlusDiv.addEventListener("click", () => {
        addTextPlusDiv.classList.add('hidden')
        addTextInputCont.classList.remove('hidden')
    })
    addTextInput.addEventListener("input", () => { saveNewText() });
}

async function saveNewText() {
    const lastValue = addTextInput.value
    await sleep(wait3sec)
    const newValue = addTextInput.value
    if (lastValue === newValue) {
        if (lastValue.length > 0) {
            const chapter = addChapterInput.value
            fetch(`/add_text/`,
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'book_id': currentBookId, 'chapter': chapter, 'text': lastValue})
            })
                .then(response => response.json())
                .then(result => {
                    if (result['result'] == 'success') {
                        console.log('lol, ok')
                    } else if (result['result'] == 'failure') {
                        console.log('lol, not ok')
                    }
                })
                // .then(await sleep(wain1sec))
                // .then(() => { window.location.reload() })
        } else {
            console.log('nope')
        }
    }
}


async function saveBookNewName() {
    const lastValue = bookRenameInput.value
    await sleep(wait3sec)
    const newValue = bookRenameInput.value
    if (lastValue === newValue) {
        if (lastValue.length > 0 && lastValue.length < 256) {
            fetch(`/rename_book/`,
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'book_name': lastValue, 'book_id': currentBookId})
            })
                // .then(response => response.json())
                // .then(result => {
                //     if (result['result'] == 'success') {
                //         console.log('lol, ok')
                //     } else if (result['result'] == 'failure') {
                //         console.log('lol, not ok')
                //     }
                // })
                // .then(await sleep(wain1sec))
                .then(() => { window.location.reload() })
        } else {
            console.log('nope')
        }
    }
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

    divBookCont.addEventListener("click", (event) => {
        bookClicked(event.target)
        loadingGif.classList.remove('hidden')
        addTextMainDiv.classList.remove('hidden')
        addTextPlusDiv.classList.remove('hidden')
        addTextInputCont.classList.add('hidden')
    })
}


function bookClicked(target) {
    let bookId = parseInt(target.getAttribute('id').replace('book', ''))
    currentBookId = bookId
    bookYesDelBtn.classList.add('hidden')
    newBookDiv.classList.add('hidden')
    bookDiv.classList.remove('hidden')
    bookRenameInput.classList.add('hidden')
    bookNameHeader.classList.remove('hidden')
    bookNameHeader.textContent = books[bookId]

    while (textsMainCont.firstChild) { textsMainCont.firstChild.remove() }

    fetch(`/get_texts/`,
    {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'book_id': currentBookId})
    })
        .then(response => response.json())
        .then(result => {
            if (result['result'] == 'success') {
                console.log('lol, ok')
                // console.log(result['data']['texts'])
                textsAndChaptersConstruct(result['data']['texts'])
            } else if (result['result'] == 'failure') {
                console.log('lol, not ok')
            }
            loadingGif.classList.add('hidden')
        })
}

function textsAndChaptersConstruct(texts) {
    let keepOneMoreOpen = 0
    for (let chapt of texts) {
        // console.log(Object.keys(chapt)[0])
        const chapterMainCont = document.createElement('DIV')
        chapterMainCont.classList.add('chapter-cont')

        const chapterHeadCont = document.createElement('DIV')
        chapterHeadCont.classList.add('chapter-head-cont')

        const chapterName = document.createElement('DIV')
        const chapterDone = document.createElement('DIV')
        chapterName.classList.add('chapter-name')
        chapterDone.classList.add('chapter-done')

        chapterName.textContent = Object.keys(chapt)[0]
        chapterHeadCont.appendChild(chapterName)
        chapterHeadCont.appendChild(chapterDone)


        chapterHeadCont.addEventListener("click", (event) => {
            // console.log(event.target)
            // console.log(event.target.parentElement.childNodes)
            for (let i=1; i<event.target.parentElement.childNodes.length; i++) {
                // console.log(event.target.parentElement.childNodes[i])
                event.target.parentElement.childNodes[i].classList.toggle('hidden')
            }
        })

        chapterMainCont.appendChild(chapterHeadCont)
        let textSum = 0
        let doneSum = 0
        for (let text of chapt[Object.keys(chapt)[0]]) {
            textSum++
            // console.log(Object.keys(chapt)[0], text)
            // console.log(text['text_preview'])
            const chapterTextContHide = document.createElement('DIV')
            chapterTextContHide.classList.add('chapter-text-cont-hide')

            const chapterTextCont = document.createElement('DIV')
            chapterTextCont.classList.add('chapter-text-cont')
            chapterTextCont.setAttribute('id', 'text'+text['text_id']);

            const chapterTextText = document.createElement('DIV')
            const chapterTextDone = document.createElement('DIV')
            chapterTextText.classList.add('chapter-text-text')
            chapterTextDone.classList.add('chapter-text-done')
            chapterTextText.textContent = text['text_preview']
            if (text['done'] == true) {
                doneSum++
                chapterTextDone.textContent = '✅'
            } else {
                chapterTextDone.textContent = '❌'
            }

            chapterTextCont.appendChild(chapterTextText)
            chapterTextCont.appendChild(chapterTextDone)

            chapterTextContHide.appendChild(chapterTextCont)
            chapterMainCont.appendChild(chapterTextContHide)

            chapterTextCont.addEventListener("click", (event) => {
                let id = event.target.id.replace('text', '')
                window.location.href = '/type/' + id
            })
        }
        // console.log(texts)
        if (textSum === doneSum) {
            chapterDone.textContent = `Done ${doneSum} out of ${textSum} ✅`
            // console.log(chapterMainCont.childNodes)
            for (let i=1; i<chapterMainCont.childNodes.length; i++) {
                chapterMainCont.childNodes[i].classList.toggle('hidden')
            }
        } else if (doneSum > 0) {
            chapterDone.textContent = `Done ${doneSum} out of ${textSum} 🟡`
            keepOneMoreOpen++
        } else if (keepOneMoreOpen === 0) {
            chapterDone.textContent = `Done ${doneSum} out of ${textSum}  `
            keepOneMoreOpen++
        } else {
            chapterDone.textContent = `Done ${doneSum} out of ${textSum} ❌`
            for (let i=1; i<chapterMainCont.childNodes.length; i++) {
                chapterMainCont.childNodes[i].classList.toggle('hidden')
            }
        }
        textsMainCont.appendChild(chapterMainCont)
    }
    // console.log(texts)
}


function addNewBookBtn() {
    const divAddBookCont = document.createElement('DIV')
    const divBook = document.createElement('DIV')
    divAddBookCont.classList.add('book-cont')
    divAddBookCont.classList.add('book-cont-add')
    divAddBookCont.classList.add('hoverable')
    divAddBookCont.setAttribute('id', 'new')
    divBook.classList.add('book-plus')
    divBook.textContent = '+ add book...'
    divAddBookCont.appendChild(divBook)
    divBookList.appendChild(divAddBookCont)

    divAddBookCont.addEventListener("click", () => {
        newBookDiv.classList.toggle('hidden')
        bookDiv.classList.add('hidden')
    });
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
            // .then(await sleep(wain1sec))
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
            // .then(await sleep(wain1sec))
            .then(() => { window.location.reload() })
    } else {
        console.log('no book id')
    }
}

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}
