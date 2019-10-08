var client = require('./connection.js')

client.index({
  index: 'gov',
  id: '1',
  type: 'constituencies',
  body: {
    'ConstituencyName': 'Ipswich',
    'ConstituencyID': 'E14000761',
    'ConstituencyType': 'Borough',
    'Electorate': 74499,
    'ValidVotes': 48694
  }
}, function (_err, resp, _status) {
  console.log(resp)
})
