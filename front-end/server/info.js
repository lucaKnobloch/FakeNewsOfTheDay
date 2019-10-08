var client = require('./server.js')

client.cluster.health({}, function (_err, resp, _status) {
  console.log('-- Client Health --', resp)
})

client.count({index: 'news-english', type: 'article'}, function (_err, resp, _status) {
  console.log('news-english', resp)
})
