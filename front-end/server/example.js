'use strict'

const { Client } = require('@elastic/elasticsearch')
const client = new Client({ node: 'http://0.0.0.0:9200' })

async function run () {
  const { body } = await client.search({
    index: 'news-english',
    body: {query: {
      'match': {
        'published': '2019-08-13T16:22:31Z'
      }
    }
    }
  })

  console.log(body.hits.hits)
}

run().catch(console.log)
