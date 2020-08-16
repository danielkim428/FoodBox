document.addEventListener('DOMContentLoaded', () => {
  console.log('Scripts loaded. ')

  ////////////////////////////////////////////////////////////////
  //                                                            //
  //                        MAIN CODE                           //
  //                                                            //
  ////////////////////////////////////////////////////////////////
  /* IMPORTANT VARIABLES - Order list */
  // This orderDiv isn't that useful right now but keep it here for now
  const orderDiv = document.querySelector('#order-div')

  const orderList = orderDiv.querySelector('#order-list')
  const totalPrice = orderDiv.querySelector('#total-price')

  /* IMPORTANT MOBILE VARIABLES - Order list */
  const MOBorderDiv = document.querySelector('#MOBorder-div')

  const MOBorderList = MOBorderDiv.querySelector('#MOBorder-list')
  const MOBtotalPrice = MOBorderDiv.querySelector('#MOBtotal-price')

  /* Menu items can easily be ordered using a side div */
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

  const orderListId = document.getElementById('order-id')
  const orderButton = document.querySelector('#order-button')
  const MOBorderListId = document.getElementById('MOBorder-id')
  const MOBorderButton = document.querySelector('#MOBorder-button')

  ////////////////////////////////////////////////////////////////
  //                                                            //
  //                        FUNCTIONS                           //
  //                                                            //
  ////////////////////////////////////////////////////////////////

  /* UPDATE Count of OrderItem */
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

          totalPrice.innerHTML = result['totalPrice']
          MOBtotalPrice.innerHTML = result['totalPrice']

          // Update counter + get the new count
          const newCount = updateCount(counter, -1)

          const orderId = result['orderId']
          const orderItem = document.getElementById(`order-item-${orderId}`)
          const MOBorderItem = document.getElementById(`MOBorder-item-${orderId}`)

          if (newCount <= 0) {
            btn.disabled = true
            btn.classList.add('button-disabled')
            orderItem.remove()
            MOBorderItem.remove()
          }
          else {
            // Update count on the ORDER LIST
            const itemCount = orderItem.querySelector('.item-count')
            const itemPrice = orderItem.querySelector('.item-price')
            itemPrice.innerHTML = itemPrice.innerText - itemPrice.innerText / Number(itemCount.innerText)
            itemCount.innerHTML = Number(itemCount.innerText) - 1

            const MOBitemCount = MOBorderItem.querySelector('.MOBitem-count')
            const MOBitemPrice = MOBorderItem.querySelector('.MOBitem-price')
            MOBitemPrice.innerHTML = MOBitemPrice.innerText - MOBitemPrice.innerText / Number(MOBitemCount.innerText)
            MOBitemCount.innerHTML = Number(MOBitemCount.innerText) - 1
          }

          // Is the Order list none?
          if (result['none']) {
            orderButton.style.display = 'none'
            MOBorderButton.style.display = 'none'
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

          totalPrice.innerHTML = result['totalPrice']
          MOBtotalPrice.innerHTML = result['totalPrice']

          const newCount = updateCount(counter, 1)

          const orderId = result['orderId']
          // Has a new OrderItem has been created?
          if (result['new'] == true) {
            // TODO Add new order template
            orderList.innerHTML += `\
              <tr id="order-item-${ orderId }"><td class="font-weight-bold">${ result['name'] }</td><td class="text-right item-count">1</td><td class="text-right item-price">${ result['price'] }</td></tr>`

            MOBorderList.innerHTML += `\
              <tr id="MOBorder-item-${ orderId }"><td class="font-weight-bold">${ result['name'] }</td><td class="text-right MOBitem-count">1</td><td class="text-right MOBitem-price">${ result['price'] }</td></tr>`

            // Add the OrderItem ID to the remove item button
            removeBtn.dataset.id = orderId
            removeBtn.disabled = false
            removeBtn.classList.remove('button-disabled')
          }
          else {
            const orderItem = document.getElementById(`order-item-${orderId}`)
            const itemCount = orderItem.querySelector('.item-count')
            itemCount.innerHTML = Number(itemCount.innerText) + 1

            const itemPrice = orderItem.querySelector('.item-price')
            itemPrice.innerHTML = Number(itemPrice.innerHTML) + result['price']

            const MOBorderItem = document.getElementById(`MOBorder-item-${orderId}`)
            const MOBitemCount = MOBorderItem.querySelector('.MOBitem-count')
            MOBitemCount.innerHTML = Number(MOBitemCount.innerText) + 1

            const MOBitemPrice = MOBorderItem.querySelector('.MOBitem-price')
            MOBitemPrice.innerHTML = Number(MOBitemPrice.innerHTML) + result['price']
          }

          // If a new Order object has been created, enable
          if (result['newOrderList']) {
            console.log(result['orderListId'])
            orderListId.value = result['orderListId']
            orderButton.style.display = 'block'

            MOBorderListId.value = result['orderListId']
            MOBorderButton.style.display = 'block'
          }
        })
    }
  }

  ////////////////////////////////////////////////////////////////
  //                                                            //
  //                      LEGACY CODE                           //
  //                                                            //
  ////////////////////////////////////////////////////////////////
  // Don't delete what's underneath unless instructed to.

  // // Call all the add-order-button's
  // const addOrderButtons = document.querySelectorAll('.add-order-button')
  //
  // // addOrderButtons.forEach(btn => {
  // //   addOrderItem(btn)
  // // })
});
