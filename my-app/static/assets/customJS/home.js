const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

function eliminarProducto(id_producto) {
  if (confirm("¿Estas seguro que deseas Eliminar el producto?")) {
    let url = `/borrar-producto/${id_producto}`;
    if (url) {
      window.location.href = url;
    }
  }
}
