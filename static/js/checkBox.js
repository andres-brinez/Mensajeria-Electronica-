

// función para seleccionar solo un checkbox  -  función anónima y tipo flecha

( () => {

    let checkboxes = document.querySelectorAll('input[type="checkbox"]')

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            checkboxes.forEach(function(otherCheckbox) {
                if (otherCheckbox !== checkbox)
                    otherCheckbox.checked = false
            })
        })
    });
} ) ();








