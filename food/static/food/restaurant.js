document.addEventListener('DOMContentLoaded', () => {
  console.log('Scripts loaded. ')

  ////////////////////////////////////////////////////////////////
  //                                                            //
  //                        FUNCTIONS                           //
  //                                                            //
  ////////////////////////////////////////////////////////////////

  /* UPDATE Count of OrderItem */
  // I mean, this is pretty useless but I don't know maybe
  // bump: the number you want to add to the item count (can be negative)
  function updateCount(counter, bump) {
    const count = Number(counter.innerHTML)
    counter.innerHTML = count + bump

    return count + bump
  }

  /* REMOVE OrderItem button functionality */
  function removeOrderItem(btn, counter) {
    btn.onclick = () => {
      const orderItemId = btn.dataset.id

      // Call removeItem API
      fetch(`/api/menu/removeOrderItem/${orderItemId}`)
        .then(response => response.json())
        .then(result => {
          console.log(result)

          // Update counter + get the new count
          const newCount = updateCount(counter, -1)

          if (newCount <= 0) {
            btn.disabled = true
          }
        })
    }
  }

  /* ADD OrderItem button functionality */
  function addOrderItem(btn, removeBtn, counter) {
    btn.onclick = () => {
      // Data to send to back-end
      const menuId = btn.dataset.id
      const restaurantId = btn.dataset.restaurantid

      // Call addItem API
      fetch(`/api/menu/addOrderItem/${restaurantId}/${menuId}`)
        .then(response => response.json())
        .then(result => {
          console.log(result)

          const newCount = updateCount(counter, 1)

          // Has a new OrderItem has been created?
          if (result['new'] == true) {
            const orderId = result['orderId']

            // Add the OrderItem ID to the remove item button
            removeBtn.dataset.id = orderId
            removeBtn.disabled = false
          }
        })
    }
  }

  ////////////////////////////////////////////////////////////////
  //                                                            //
  //                        MAIN CODE                           //
  //                                                            //
  ////////////////////////////////////////////////////////////////

  /* FEATURE 1: Menu items can easily be ordered using a side div */

  // Call the order item divs
  const itemDivs = document.querySelectorAll('.order-item-div')
  itemDivs.forEach(itemDiv => {
    const counter = itemDiv.querySelector('.order-item-count')

    // - Remove-order buttons
    const removeButton = itemDiv.querySelector('.remove-order-button')
    removeOrderItem(removeButton, counter)

    // + Add-order buttons
    const addButton = itemDiv.querySelector('.add-order-button')
    addOrderItem(addButton, removeButton, counter)
  })

  /* LEGACY CODE */
  // Don't delete what's underneath unless instructed to.

  // // Call all the add-order-button's
  // const addOrderButtons = document.querySelectorAll('.add-order-button')
  //
  // // addOrderButtons.forEach(btn => {
  // //   addOrderItem(btn)
  // // })
});
