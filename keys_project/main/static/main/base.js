const dark_mode_checkbox = document.querySelector('.dark_mode_checkbox')
const options = JSON.parse(document.getElementById('options').textContent)

const csrftoken_options = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

onInit()

// dark_mode_checkbox.addEventListener("input", () => {
//     dark_mode_checkbox.setAttribute('disabled', 'disabled')
// });

function onInit() {
    dark_mode_checkbox.checked = options['dark_mode']
    setColors(dark_mode_checkbox.checked)
    dark_mode_checkbox.addEventListener("input", () => { setOptions() });
}

function setOptions() {
    dark_mode_checkbox.setAttribute('disabled', 'disabled')
    fetch(`/set_options/`,
    {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken_options,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'dark_mode': dark_mode_checkbox.checked})
    })
    .then(response => {
        if (response.status === 204) {
            dark_mode_checkbox.removeAttribute('disabled')
            setColors(dark_mode_checkbox.checked)
        }
    })
}

function setColors(darkMode) {
    const paintBody = document.querySelector('body')
    // const paintOuterBox = document.querySelectorAll('.outer-box')
    // const paintMenuButton = document.querySelectorAll('.menu-button')
    // const paintMenuButtonA = document.querySelectorAll('.menu-button > a')
    // const paintOptionsDropDown = document.querySelector('.options-content-hide')
    if (darkMode === true) {
        paintBody.classList.remove('light'); paintBody.classList.add('night')
        // paintOptionsDropDown.classList.remove('light'); paintOptionsDropDown.classList.add('night')
        // for (let elem of paintOuterBox) { elem.classList.remove('light'); elem.classList.add('night') }
        // for (let elem of paintMenuButton) { elem.classList.remove('light'); elem.classList.add('night') }
        // for (let elem of paintMenuButtonA) { elem.classList.remove('light'); elem.classList.add('night') }
    } else if (darkMode === false) {
        paintBody.classList.remove('night'); paintBody.classList.add('light')
        // paintOptionsDropDown.classList.remove('night'); paintOptionsDropDown.classList.add('light')
        // for (let elem of paintOuterBox) { elem.classList.remove('night'); elem.classList.add('light') }
        // for (let elem of paintMenuButton) { elem.classList.remove('night'); elem.classList.add('light') }
        // for (let elem of paintMenuButtonA) { elem.classList.remove('night'); elem.classList.add('light') }
    }
}
