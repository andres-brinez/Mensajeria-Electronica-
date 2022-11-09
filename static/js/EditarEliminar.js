// con tipo indicamos si es editar o eliminar
function EditarEliminar(tipo){

    try{

        // saber cual checkbox esta seleccionado
        let checkboxSeleccionado = document.querySelector('input[type="checkbox"]:checked');

        // el value del checkbox es el id de la empresa
        let id = checkboxSeleccionado.value;

        if (tipo === "eliminar") {

            console.log(typeof(id))
            Swal.fire({
                title: "¿Está seguro que desea eliminar este mensaje",
                text: "No podras revertir esto!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Si',
                cancelButtonText: 'Cancelar'
            })
                .then((result) => {
                    if (result.isConfirmed) {
                        //redireciona a la página indicada con el atributo id
                        window.location.href = "/delete/" + id;
                    }

                })
        }
        else if (tipo === "editar") {

            // redireciona a la página indicada con el atributo id
            window.location.href = "/edit/" + idEmpresa;
        }
    }

    catch (e) {
        // si no hay ningun checkbox seleccionado
        Swal.fire({
            title: 'No hay ningún mensaje seleccionado',
            text: "Seleccione para poder realizar esta acción",
            icon: 'question',

        })
    }

}

const buttonEliminar = document.querySelector(".btnEliminar")
buttonEliminar.addEventListener("click", function(e) {
    e.preventDefault()
    EditarEliminar("eliminar" )
    }
    )

const buttonEditar = document.querySelector('.btnEditar');
buttonEditar.addEventListener('click', function(e){
    e.preventDefault()
    EditarEliminar("editar")
    }
);