document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded.')

  const phoneForm = document.querySelector('#submitPhone')
  const header = document.querySelector('.changeableText')
  const otpForm = document.querySelector('#otpForm')

  phoneForm.onsubmit = () => {
    const number = phoneForm.phoneNumber.value

    if (number != '' && number.length == 10) {
      phoneForm.style.display = 'none'
      header.innerHTML = `An OTP has been sent to <b>${number}</b> through WhatsApp.`
      otpForm.style.display = 'block'
      otpForm.phoneNumber.value = number

      fetch(`/api/phoneNumber/${number}`)
        .then(response => response.json())
        .then(result => {
          console.log(result)
        })
    }

    return false
  }
})
