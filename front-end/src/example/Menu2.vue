<template lang="pug">
  #menu2
    ul.test-menu(v-if="setts") 
      li
        label Amount of entities:
          span {{ setts.maxNodes }}
        input(type="range" v-model.number="setts.maxNodes" @input="change" min="0" max="30" step="3")    
      li
        button.btn(@click="$emit('simulate')") Simulate
      //- disables further options which do not support more information
      //- li
      //-   label Node Size:
      //-     span {{ opts.nodeSize }}
      //-   input(type="range" v-model.number="opts.nodeSize" @input="change" min="3" max="100" step="1")
      //- li
      //-   label Link Thickness:
      //-     span {{ opts.linkWidth }}
      //-   input(type="range" v-model.number="opts.linkWidth" @input="change" min="1" max="15" step="1")
      //- li
      //-   label Render type
      //- li
      //-   input(type='radio' :value='false' v-model='opts.canvas' id='svg-rad' @change="change")
      //-   label(for='svg-rad') svg
      //-   input(type='radio' :value='true' v-model='opts.canvas' id='canvas-rad' @change="change")
      //-   label(for='canvas-rad') canvas
      

    ul.test-menu
      li
        label Offset Y:
          span {{ opts.offset.y }}
        input(type="range" v-model.number="opts.offset.y" @input="change" min="-250" max="250" step="1")
      li
        label Offset X:
          span {{ opts.offset.x }}
        input(type="range" v-model.number="opts.offset.x" @input="change" min="-250" max="250" step="1")

    ul.test-menu
      li
        label Force:
          span {{ opts.force }}
        input(type="range" v-model.number="opts.force" @input="change" min="1" max="5000" step="1")
      li
        button.btn(@click="reset" title="reset options")
          span(class="icon-reset")
          small &nbsp;Reset      
      //- li
      //-   input(type="checkbox" v-model="opts.nodeLabels" @change="change")
      //-   label Show node names
      //- li
      //-   input(type="checkbox" v-model="opts.linkLabels" @change="change")
      //-   label Show link names
      
     
      //- li(v-if="opts.nodeLabels || opts.linkLabels")
      //-   label Font Size:
      //-     span {{ opts.fontSize }}
      //-   input(type="range" v-model.number="opts.fontSize" @input="change" min="1" max="30" step="1")
      //- li
      //-   input(type="checkbox" v-model="opts.strLinks" @change="change")
      //-   label Straight Links


</template>
<script>
import defaultData from './data.js'
export default {
  name: 'd3-net-menu2',
  props: ['links', 'nodes', 'settings', 'options'],
  data () {
    let data = Object.assign({}, defaultData)
    return {
      opts: data.options,
      setts: null,
    }
  },
  created () {
    this.opts = this.options
    this.setts = this.settings
  },
  methods: {
    change () {
      this.$emit('options', this.opts)
      this.$emit('settings', this.setts)
      
    },
    reset () {
      this.opts = Object.assign({}, defaultData.options)
      this.options.width = this.$el.clientWidth
      this.options.height = this.$el.clientHeight
      this.$emit('reset', this.options)
    },
    emit (e) {
      this.$emit(e)
    }
  }
}
</script>
<style src="../assets/css/icons.css"></style>
<style lang="stylus" scoped>
 @import '../lib/styl/vars.styl'
.debug
  font-size: 0.5em
  list-style: none

.test-menu
  display: table-cell
  padding: 1em
  list-style: none
  li
    margin: 0.5em 0
    label
      font-size: 0.85em
      display: block
      span
        font-weight: normal
    input + label
      display: inline
      margin-left: .5em

ul.test-menu + ul.test-menu
  border-left: none

</style>
