document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM content loaded.');

    function addOrderItem(btn) {
      // When clicked, call addOrder API
      btn.onclick = () => {
        const menuId = btn.dataset.id
        const restaurantId = btn.dataset.restaurantid

        fetch(`/api/menu/addOrderItem/${restaurantId}/${menuId}`)
          .then(response => response.json())
          .then(result => {
            console.log(result)
          })
      }
    }

    // Call all the add-order-button's
    const addOrderButtons = document.querySelectorAll('.add-order-button');

    addOrderButtons.forEach(btn => {
      addOrderItem(btn)
    })
});
