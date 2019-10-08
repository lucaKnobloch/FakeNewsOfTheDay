var client = require('./connection.js')

client.delete({
  index: 'gov',
  id: '1',
  type: 'constituencies'
}, function (_err, resp, status) {
  console.log(resp)
})
