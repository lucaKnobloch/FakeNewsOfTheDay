/* eslint-disable no-console */
import axios from 'axios'
// Base URL to connect with the Flask Server
const API_URL = 'http://0.0.0.0:5000'

// axios config to enable CORS functionalty
// sets the header as well 
let axiosConfig = {
  headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      "Access-Control-Allow-Origin": "*",
  }
};

// find links by node => [ links ] | null
export const findLinks = (nodeId, links) => {
  let nodeLinks = []
  for (let link of links) {
    if (link.sid === nodeId || link.tid === nodeId) nodeLinks.push(link)
  }
  return (nodeLinks.length) ? nodeLinks : null
}

// find Node by index 
export const findNode = (nodes, nodeId) => {
  let index = nodeExists(nodeId)
  if (index) {
    return nodes[index]
  }
  return null
}

// removes node by id => () => ( [newNodes] )
export const removeNode = (nodeId, nodes, cb) => {
  let index = nodes.findIndex(
    (node) => { return node.id === nodeId }
  )
  if (index > -1) {
    nodes.splice(index, 1)
    cb(nodes)
  } else {
    cb(null)
  }
}

// removes orphaned links => { newLinks, removed }
export const rebuildLinks = (nodes, links) => {
  let newLinks = []
  let removed = []
  for (let link of links) {
    if (nodeExists(link.sid, nodes) && nodeExists(link.tid, nodes)) {
      newLinks.push(link)
    } else {
      removed.push(link)
    }
  }
  return { newLinks, removed }
}

// removes unlinked nodes => [ newNodes ]
export const rebuildNodes = (links, nodes) => {
  let newNodes = []
  for (let node of nodes) {
    if (isLinked(node.id, links)) {
      newNodes.push(node)
    }
  }
  return newNodes
}

// finds node by id => boolean
export const nodeExists = (nodeId, nodes) => {
  let index = nodes.findIndex(
    (node) => { return node.id === nodeId }
  )
  return (index > -1)
}

// Checks if node is linked => boolean
const isLinked = (nodeId, links) => {
  let index = links.findIndex(
    (link) => { return (link.tid === nodeId || link.sid === nodeId) }
  )
  return (index > -1)
}

// link formatter
export const newLink = (id, sid, tid) => {
  return { id, sid, tid }
}
export const newLink2 = (id, sid, tid) => {
  return { id, sid, tid }
}

// generates links => [ links ]
// export const makeLinks = (nodes, maxLinks) => {
export const makeLinks = (nodes) => {
  let links = []
  let index = 0
  let iter = 2
  let maxAmountOfLinks = nodes.length
  for (let i = 0; i < maxAmountOfLinks; i++) {
    let target = Math.floor(index)
    let source = i
    if (i === iter) {
      index += 3
      iter += 3
    }
    links.push(newLink(i, source, target))
  }
  return links
}

// generates links for the fake graph => [ links ]
export const makeLinks2 = (nodes) => {
  let links = []
  let index = 0
  let iter = 2
  let maxAmountOfLinks = nodes.length
  for (let i = 0; i < maxAmountOfLinks; i++) {
    let target = Math.floor(index)
    let source = i
    if (i === iter) {
      index += 3
      iter += 3
    }
    links.push(newLink2(i, source, target))
  }
  return links
}

export const formatDate = (date) => {
   // formats the input date to the format which is necessary 
   var tmpDate = date.getDate() + '-' + (date.getMonth() + 1) + '-' + date.getFullYear()
   // adds 0 at the beginning if there is none
   var check = tmpDate.charAt(1)
   if (check === '-') {
     tmpDate = 0 + tmpDate
   }
   return tmpDate
}

export const indexEntities = (nodeId, index, i ) => {
  if (nodeId > 2) {
    i += 1
    index -= 3
    // take the next article
    if (nodeId > 5) {
      i = 2
      index -= 3
    }
    if (nodeId > 8) {
      i = 3
      index -= 3
    }
    if (nodeId > 11) {
      i = 4
      index -= 3
    }
    if (nodeId > 14) {
      i = 5
      index -= 3
    }
    if (nodeId > 17) {
      i = 6
      index -= 3
    }
    if (nodeId > 20) {
      i = 7
      index -= 3
    }
    if (nodeId > 23) {
      i = 8
      index -= 3
    }
    if (nodeId > 26) {
      i = 9
      index -= 3
    }
    if (nodeId > 29) {
      i = 10
      index -= 3
    }
    if (nodeId > 32) {
      i = 11
      index -= 3
    }
  }
  return (index, i)
}

// Methods are seperated to each graph because of render issues
export const NewDataFromElastic = (nodeId, date, news) => {
  var entities = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  // sends a request to get the data from elasticsearch 
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    var index = nodeId
    // checks if the date is the same 
    if (res.data[0]._source.date === tmpDate) {
      // 3 entites per network and it starts with 0
      if (nodeId > 2) {
        i += 1
        index -= 3
        // take the next article
        if (nodeId > 5) {
          i = 2
          index -= 3
        }
        if (nodeId > 8) {
          i = 3
          index -= 3
        }
        if (nodeId > 11) {
          i = 4
          index -= 3
        }
        if (nodeId > 14) {
          i = 5
          index -= 3
        }
        if (nodeId > 17) {
          i = 6
          index -= 3
        }
        if (nodeId > 20) {
          i = 7
          index -= 3
        }
        if (nodeId > 23) {
          i = 8
          index -= 3
        }
        if (nodeId > 26) {
          i = 9
          index -= 3
        }
        if (nodeId > 29) {
          i = 10
          index -= 3
        }
        if (nodeId > 32) {
          i = 11
          index -= 3
        }
      }
      // saves from the responds the entity.
      // since the entites are 
      let entity = res.data[i]._source.entities[index]

      // ensures that not null entities are sent 
      if (entity != undefined) {
        entities.push(entity)
      }   
     
    }
  })
  return entities
}

// unforntunalty not working if you apply this. It gets undefinied errors
export const indexUrl = (nodeId, i) => {
  if (nodeId > 2) {
    i += 1
    // take the next article
    if (nodeId > 5) {
      i = 2
    }
    if (nodeId > 8) {
      i = 3
    }
    if (nodeId > 11) {
      i = 4
    }
    if (nodeId > 14) {
      i = 5
    }
    if (nodeId > 17) {
      i = 6
    }
    if (nodeId > 20) {
      i = 7
    }
    if (nodeId > 23) {
      i = 8
    }
    if (nodeId > 26) {
      i = 9
    }
    if (nodeId > 29) {
      i = 10
    }
    if (nodeId > 32) {
      i = 11
    }
  return i
  }
}

// returns the url of the entites
export const NewUrlFromElastic = (nodeId, date, news) => {
  var urls = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    if (res.data[0]._source.date === tmpDate){
    // 3 entites per network and it starts with 0
    if (nodeId > 2) {
      i += 1
      // take the next article
      if (nodeId > 5) {
        i = 2
      }
      if (nodeId > 8) {
        i = 3
      }
      if (nodeId > 11) {
        i = 4
      }
      if (nodeId > 14) {
        i = 5
      }
      if (nodeId > 17) {
        i = 6
      }
      if (nodeId > 20) {
        i = 7
      }
      if (nodeId > 23) {
        i = 8
      }
      if (nodeId > 26) {
        i = 9
      }
      if (nodeId > 29) {
        i = 10
      }
      if (nodeId > 32) {
        i = 11
      }
    }
    let url = res.data[i]._source.url
    urls.push(url)
  }
  })
  return urls
}

// retuns the occurance of the entitie insinde of the text 
export const NewContentFromElastic = (nodeId, date, news) => {
  var contents = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    // eslint-disable-next-line no-unused-vars
    var index = nodeId
    if (res.data[0]._source.date === tmpDate) {
      // get the right index
      if (nodeId > 2) {
        i += 1
        index -= 3
        // take the next article
        if (nodeId > 5) {
          i = 2
          index -= 3
        }
        if (nodeId > 8) {
          i = 3
          index -= 3
        }
        if (nodeId > 11) {
          i = 4
          index -= 3
        }
        if (nodeId > 14) {
          i = 5
          index -= 3
        }
        if (nodeId > 17) {
          i = 6
          index -= 3
        }
        if (nodeId > 20) {
          i = 7
          index -= 3
        }
        if (nodeId > 23) {
          i = 8
          index -= 3
        }
        if (nodeId > 26) {
          i = 9
          index -= 3
        }
        if (nodeId > 29) {
          i = 10
          index -= 3
        }
        if (nodeId > 32) {
          i = 11
          index -= 3
        }
      }
      let occurance = res.data[i]._source.occurance[index]
      let tmpOccurance = ".." + occurance + ".."
      contents.push(tmpOccurance)
    }
  })
  return contents
}
// returns the entities which are visiable as names
export const NewDataFromElastic2 = (nodeId, date, news) => {
  var entities = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    var index = nodeId
    if (res.data[0]._source.date === tmpDate) {
    // 3 entites per network and it starts with 0
    // get the right index
    if (nodeId > 2) {
      i += 1
      index -= 3
      // take the next article
      if (nodeId > 5) {
        i = 2
        index -= 3
      }
      if (nodeId > 8) {
        i = 3
        index -= 3
      }
      if (nodeId > 11) {
        i = 4
        index -= 3
      }
      if (nodeId > 14) {
        i = 5
        index -= 3
      }
      if (nodeId > 17) {
        i = 6
        index -= 3
      }
      if (nodeId > 20) {
        i = 7
        index -= 3
      }
      if (nodeId > 23) {
        i = 8
        index -= 3
      }
      if (nodeId > 26) {
        i = 9
        index -= 3
      }
      if (nodeId > 29) {
        i = 10
        index -= 3
      }
      if (nodeId > 32) {
        i = 11
        index -= 3
      }
    }
    // saves the entites 
    let entity = res.data[i]._source.entities[index]
     // ensures that not null entities are sent 
     if (entity != undefined) {
      entities.push(entity)
    } 
    }
  })
  return entities
}

export const NewUrlFromElastic2 = (nodeId, date, news) => {
  var urls = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    if (res.data[0]._source.date === tmpDate) {
    // 3 entites per network and it starts with 0
    if (nodeId > 2) {
      i += 1
      // take the next article
      if (nodeId > 5) {
        i = 2
      }
      if (nodeId > 8) {
        i = 3
      }
      if (nodeId > 11) {
        i = 4
      }
      if (nodeId > 14) {
        i = 5
      }
      if (nodeId > 17) {
        i = 6
      }
      if (nodeId > 20) {
        i = 7
      }
      if (nodeId > 23) {
        i = 8
      }
      if (nodeId > 26) {
        i = 9
      }
      if (nodeId > 29) {
        i = 10
      }
      if (nodeId > 32) {
        i = 11
      }
    let url = res.data[i]._source.url
    urls.push(url)
    }}
  })
  return urls
}

export const NewContentFromElastic2 = (nodeId, date, news) => {
  var contents = []
  // formats the date into the right format for the request
  var tmpDate = formatDate(date)
  axios.post(`${API_URL}/search/${tmpDate}/${news}`, axiosConfig).then(function (res) {
    var i = 0
    // eslint-disable-next-line no-unused-vars
    var index = nodeId
    if (res.data[0]._source.date === tmpDate & res.data[i]._source.entities[nodeId] !== '') {
      // get the right index
      if (nodeId > 2) {
        i += 1
        index -= 3
        // take the next article
        if (nodeId > 5) {
          i = 2
          index -= 3
        }
        if (nodeId > 8) {
          i = 3
          index -= 3
        }
        if (nodeId > 11) {
          i = 4
          index -= 3
        }
        if (nodeId > 14) {
          i = 5
          index -= 3
        }
        if (nodeId > 17) {
          i = 6
          index -= 3
        }
        if (nodeId > 20) {
          i = 7
          index -= 3
        }
        if (nodeId > 23) {
          i = 8
          index -= 3
        }
        if (nodeId > 26) {
          i = 9
          index -= 3
        }
        if (nodeId > 29) {
          i = 10
          index -= 3
        }
        if (nodeId > 32) {
          i = 11
          index -= 3
        }
      }
      let occurance = res.data[i]._source.occurance[index]
      let tmpOccurance = ".." + occurance + ".."
      contents.push(tmpOccurance)
      }
  })
  return contents
}
// create new Real node
export const newRealNode = (nodeId, date) => {
  var news = true
  var realElasticNode = NewDataFromElastic(nodeId, date, news)
  var realElasticNodeUrl = NewUrlFromElastic(nodeId, date, news)
  var realElasticNodeContent = NewContentFromElastic(nodeId, date, news)
  return { id: nodeId, name: realElasticNode, url: realElasticNodeUrl, content: realElasticNodeContent }
}

// generates nodes => [ nodes ]
export const makeRealNodes = (maxNodes, date) => {
  let nodes = Array.apply(null, { length: maxNodes })
    .map((value, index) => { return newRealNode(index, date) })
  return nodes
}

// create new Fake node
export const newFakeNode = (nodeId, date) => {
  var news = false
  var fakeElasticNodeName = NewDataFromElastic2(nodeId, date, news)
  var fakeElasticNodeUrl = NewUrlFromElastic2(nodeId, date, news)
  var fakeElasticNodeContent = NewContentFromElastic2(nodeId, date, news)
  return { id: nodeId, name: fakeElasticNodeName, url: fakeElasticNodeUrl, content: fakeElasticNodeContent }
}

// generates Nodes which are classified as wrong
export const makeFakeNodes = (maxNodes, date) => {
  let nodes = Array.apply(null, { length: maxNodes })
    .map((value, index) => { return newFakeNode(index, date) })
  return nodes
}
// vue custom event handler
export const methodCall = (vm, action, args) => {
  let method = vm[action]
  if (typeof method === 'function') {
    if (args) method(...args)
    else method()
  } else {
    // eslint-disable-next-line no-console
    console.error('Call to undefined method:', action)
  }
}

// vue event wrapper
export const emitEvent = (vm, action, args) => {
  if (vm.$data.conf && vm.$data.conf.allEventsAs) {
    let evName = vm.$data.conf.allEventsAs
    return vm.$emit(evName, action, args)
  }
  return vm.$emit(action, ...args)
}
