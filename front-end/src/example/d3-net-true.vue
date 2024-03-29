<template lang="pug">
  #example(@keyup.esc='setTool("pointer")')
    //-> Network
    d3-network(
    ref='net'
    :net-nodes="nodes"
    :net-links="links"
    :selection="{nodes: selected, links: linksSelected}"
    :options="options"
    :linkCb="linkCb"
    :node-sym='nodeSym'
    @node-click="nodeClick"
    @screen-shot='screenShotDone'
    )
    //-> Menu
    .over
      .menu-net(v-if="showMenu")
        .close(@click="setShowMenu(false)")
        d3-net-menu(
          :nodes="nodes"
          :links="links"
          :settings="settings"
          :options="options"
          @simulate="reset"
          @reset="resetOptions"
          )

      .options.menu(v-else)
        ul.inline
          normal <p> Entites classified as Real</p>
          //-normal <p> Settings </p>
        ul.inline
        <p> </p>
          button.menu(@click="setShowMenu(true)")
            span(class="icon-equalizerh")

    //-> toaster
    .toaster(v-if='toaster')
      p {{toaster}}
    //-> Svg export dialog
    .dialog-container(v-if='svgChoice')
      .dialog
        h5 Export as:
        input(id='to-svg' type='radio' :value='true' v-model='toSvg')
        label(for='to-svg') svg
        input(id='to-png' type='radio' :value='false' v-model='toSvg')
        label(for='to-png') png
        .buttons
          button.btn(@click='takeScreenShot') Export
          button.btn(@click='svgChoice=false') Cancel
    //-> Tools
    .tools
      ul
        li(v-for='t,to in tools')
          button.circle(@click='setTool(to)' :class='buttonClass(to)')
            span(:class='t.class' )
        li
          button.circle(@click='screenShot')
            span.icon-camera
      .tip {{ tools[tool].tip }}

    //-> Selection
    selection( v-if='showSelection'
      @action="selectionEvent"
      :data="selection()")
    
</template>
<script>
import * as utils from "./utils.js";
import defaultData from "./data.js";
import D3Network from "../vue-d3-network.vue";
import D3NetMenu from "./Menu.vue";
import Selection from "./Selection.vue";
import Example from './Example.vue'

export default {
  props:['myProp'],
  name: "d3-net-true",
  components: {
    D3Network,
    D3NetMenu,
    Selection,
    defaultData,
    utils,
    Example
  },
  data() {
    let data = Object.assign({}, defaultData);
    data.tools = {
      pointer: {
        tip: "Select",
        class: "icon-pointer"
      },
      pin: {
        tip: "click on node to pin / unpin ",
        class: "icon-pin"
      }
    };
    data.app = process.env.APP;
    data.tool = "pointer";
    data.lastNodeId = 0;
    data.lastLinkId = 0;
    data.settings = {
      maxLinks: 3,
      maxNodes: 9
    };
    data.date = this.myProp;  
    data.showHint = true;
    data.toaster = null;
    data.svgChoice = false;
    data.toSvg = false;
    data.options.icon = false;
    data.nodeSym = null
    return data;
  },
  mounted() {
    this.options.size.w = this.$el.clientWidth;
    this.options.size.h = this.$el.clientHeight;
  },
  watch: {
    myProp:function(val){
      this.selected = {};
      this.linksSelected = {};
      this.nodes = utils.makeRealNodes(this.settings.maxNodes, val);
      this.lastNodeId = this.nodes.length + 1;
      this.links = utils.makeLinks2(this.nodes, this.settings.maxLinks);
      this.lastLinkId = this.links.length + 1;
    },
    settings:function(val){
      this.selected = {};
      this.linksSelected = {};
      this.nodes = utils.makeRealNodes(this.settings.maxNodes, val);
      this.lastNodeId = this.nodes.length + 1;
      this.links = utils.makeLinks2(this.nodes, this.settings.maxLinks);
      this.lastLinkId = this.links.length + 1;
    },
    options:function(val){
      this.selected = {};
      this.linksSelected = {};
      this.nodes = utils.makeRealNodes(this.settings.maxNodes, val);
      this.lastNodeId = this.nodes.length + 1;
      this.links = utils.makeLinks2(this.nodes, this.settings.maxLinks);
      this.lastLinkId = this.links.length + 1;
    }
  },
  created() {
    this.reset();
  },
  computed: {
    showSel() {
      return true;
    }
  },
  methods: {
    linkCb(link) {
      link.name = "Link " + link.id;
      return link;
    },
    screenShot() {
      if (this.options.canvas) this.takeScreenShot(false);
      else this.svgChoice = true;
    },
    takeScreenShot() {
      this.svgChoice = false;
      this.toaster = "Exporting image";
      this.$refs.net.screenShot(null, null, this.toSvg);
    },
    screenShotDone(err) {
      this.toaster = err || "Saving Screenshot...";
      let vm = this;
      window.setTimeout(() => {
        vm.toaster = null;
      }, 3000);
    },
    resetOptions() {
      this.$set(this.$data, "options", defaultData.options);
      this.options.offset.x = 0;
      this.options.offset.y = 0;
    },
    selection() {
      return {
        nodes: this.selected,
        links: this.linksSelected
      };
    },
    buttonClass(tool) {
      if (tool === this.tool) return "selected";
    },
    setTool(tool) {
      this.tool = tool;
      let cursorClass = tool === "pointer" ? "" : "cross-cursor";
      this.$el.className = cursorClass;
    },
    updateSelection() {
      this.showSelection =
        Object.keys(this.selected).length |
        Object.keys(this.linksSelected).length;
    },
    reset() {
      this.selected = {};
      this.linksSelected = {};
      this.nodes = utils.makeRealNodes(this.settings.maxNodes, this.date);
      this.lastNodeId = this.nodes.length + 1;
      this.links = utils.makeLinks(this.nodes, this.settings.maxLinks);
      this.lastLinkId = this.links.length + 1;
    },
    removeLink(link) {
      this.unSelectLink(link.id);
      this.links.splice(link.index, 1);
    },
    rebuildLinks(nodes) {
      if (!nodes) nodes = this.nodes;
      let links = utils.rebuildLinks(nodes, this.links);
      for (let link of links.removed) {
        if (this.linksSelected[link.id]) {
          delete this.linksSelected[link.id];
        }
      }
      return links.newLinks;
    },
    removeNode(nodeId) {
      utils.removeNode(nodeId, this.nodes, nodes => {
        if (nodes) {
          this.links = this.rebuildLinks(nodes);
          this.unSelectNode(nodeId);
          this.nodes = utils.rebuildNodes(this.links, nodes);
        }
      });
    },
    pinNode(node) {
      if (!node.pinned) {
        node.pinned = true;
        node.fx = node.x;
        node.fy = node.y;
      } else {
        node.pinned = false;
        node.fx = null;
        node.fy = null;
      }
      this.nodes[node.index] = node;
    },
    // -- Selection
    selectNode(node) {
      this.selected[node.id] = node;
    },
    selectNodesLinks() {
      for (let link of this.links) {
        // node is selected
        if (this.selected[link.sid] || this.selected[link.tid]) {
          this.selectLink(link);
          // node is not selected
        } else {
          this.unSelectLink(link.id);
        }
      }
    },
    nodeClick(event, node) {
      switch (this.tool) {
        case "killer":
          this.removeNode(node.id);
          break;
        case "parent":
          this.createParent(node);
          break;
        case "pin":
          this.pinNode(node);
          break;
        default:
          // selection tool
          // is selected
          if (this.selected[node.id]) {
            this.unSelectNode(node.id);
            // is not selected
          } else {
            this.selectNode(node);
          }
          this.selectNodesLinks();
          break;
      }
      this.updateSelection();
    },
    linkClick(event, link) {
      if (this.tool === "killer") {
        this.removeLink(link);
      } else {
        if (this.linksSelected[link.id]) {
          this.unSelectLink(link.id);
        } else {
          this.selectLink(link);
        }
      }
      this.updateSelection();
    },
    selectLink(link) {
      this.$set(this.linksSelected, link.id, link);
    },
    selectionEvent(action, args) {
      utils.methodCall(this, action, args);
      this.updateSelection();
    },
    clearSelection() {
      this.selected = {};
      this.linksSelected = {};
    },
    unSelectNode(nodeId) {
      if (this.selected[nodeId]) {
        delete this.selected[nodeId];
      }
      this.selectNodesLinks();
    },
    unSelectLink(linkId) {
      if (this.linksSelected[linkId]) {
        delete this.linksSelected[linkId];
      }
    },
    setShowMenu(show) {
      this.showMenu = show;
      this.showHint = false;
    }
  }
};
</script>
<style lang="stylus">
@import '../lib/styl/vars.styl';
@import '../lib/styl/node-style.styl';

body {
  overflow-x: hidden;
}

#example, .net, button {
  margin: 0;
  padding: 0;
}

.net {
  background-color: $bg;
}

.net-svg {
  fill: $bg; // sets color to image export background
}

#example {
  position: absolute;
  max-width: 49%;
  width: 49%;
  height: calc(100%);
  max-height 100%
  left: 0;
  bottom: 0;
  box-sizing: content-box;
}

button.menu {
  width: 1em;
  height: 1em;
  padding: 0;
  font-size: 2em;
  font-weight: bold;
  color: $color;
  border: $border;
  

  &:hover {
    color: $color2;
    border-color: $color2;
  }
}

.circle {
  width: 4em;
  height: 4em;
  font-weight: bold;
  border-radius: 50%;
  border: $border;
}

.connected {
  color: $color;
}

.disconnected {
  color: $warn;
}

.node.nodeodd #fill, .node.nodeodd {
  fill: red;
}

.node-label.odd {
  fill: red;
}

.over {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 560px;
  height: 15%;
  z-index: 50;
  padding: 1em;
}


.menu {
  position: relative;
  display: inline-block;
  padding-right: 3em;
  border-radius: 0.25em;
}

.options {
  max-width: 35%
  width: 35%
  max-height: 70%
  height: 70%
  border: $dark 1px solid
  border-top-width: 10px
  border-bottom-width: 5px
  padding: 1em 2em
  background-color: $color
  color: white
  box-shadow: $sh
  margin-top: 1em
  border-radius: 0.5em;
  text-align: center;
  margin-bottom: 2em;
}

.close {
  display: block;

  &:after {
    content: $sym-close;
    position: absolute;
    right: 1em;
    top: 0.5em;
    font-size: 1.25em;
    color: $color;
    font-family: sans-serif;
    text-shadow: $txt-sh;
  }

  &:hover {
    &:after {
      color: $dark;
    }
  }
}

ul.inline {
  display: inline;
  margin: 0;
  padding: 0;
  color: white;
}

.inline {
  list-style: none;

  li {
    display: inline-block;

    &:after {
      content: '/';
      margin: 0 0.5em;
    }
  }
}

.sym-pointer {
  &:after {
    content: $sym-pointer;
  }
}

.sym-kill {
  &:after {
    content: $sym-kill;
  }
}

.sym-parent {
  &:after {
    content: $sym-parent;
  }
}

.cross-cursor {
  cursor: crosshair;
}

.tools {
  position: absolute;
  bottom: 3em;
  right: 4em;
  z-index: 101;
  text-align: center;

  ul {
    list-style: none;
    margin: 0 3em 0.5em 0;
    padding: 0;

    li {
      display: inline;
      margin-left: 0.5em;
    }

    button {
      width: 3em;
      height: 3em;
      padding: 0;

      &:hover {
        border-color: $color2;
      }

      span {
        font-size: 2.5em;
        line-height: 1em;
        color: $color;

        &:hover {
          color: $color2;
        }
      }
    }
  }

  .selected {
    border-color: $color2;

    span {
      color: $color2;
    }
  }
}

.tip {
  margin-right: 1em;
  font-style: italic;
  font-size: 0.8em;
  color: white;
}

.menu-net {
  background-color: $bg-plus;
  padding: 0.5em 1em;
  border: $dark solid 2px;
  border-width: 6px 2px 3px;
  position: relative;
  margin-bottom: 1em;
  border-radius: 0.5em;

  .close {
    position: absolute;
    top: 0;
    right: 0;

    &:after {
      color: $dark;
    }

    &:hover {
      &::after {
        color: $color;
      }
    }
  }
}

.title {
  border: 1.5px $white;
  border-style: dotted none;
  padding: 0.5em 0;
  margin: 1.5em 1em 0.5em 0.5em;

  h1 {
    color: $white;
    text-shadow: $txt-sh;
  }
}

.toaster, .dialog {
  position: absolute;
  bottom: 0.5em;
  right: 2em;
  z-index: 500;
  background-color: white;
  border: $border;
  border-radius: 0.25em;
  min-width: 20em;
  box-shadow: $sh;
  animation-name: toaster-anim;
  animation-duration: 0.25s;
}

.dialog-container {
  position: absolute;
  display: flex;
  top: 0;
  left: 0;
  min-height: 100%;
  min-width: 100%;
  border: red solid 1px;
  background-color: rgba(0, 0, 0, 0.3);

  .dialog {
    width: 20em;
    min-height: 10em;
    position: relative;
    margin: auto;

    input[type='radio'], label {
      display: inline;
    }

    label {
      font-weight: bold;
    }

    .buttons {
      margin-top: 1em;
    }

    .btn {
      margin-left: 1em;
    }
  }
}

@keyframes toaster-anim {
  0% {
    opacity: 0;
    transform: scaleY(0) translateY(5em);
  }

  100% {
    opacity: 1;
    transform: scaleY(1) translateY(0);
  }
}

h2.hint {
  display: inline;
  position: absolute;
  margin-left: 1em;
  color: $light;
  font-size: 1em;
  font-style: italic;
  letter-spacing: 0.125em;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5), 2px 2px 15px $color2;
  opacity: 0;
  animation-name: hint-anim;
  animation-delay: 1s;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;

  .icon {
    font-size: 3em;
    line-height: 0.5em;
  }
}

@keyframes hint-anim {
  0% {
    opacity: 0;
    transform: translateX(6em);
    letter-spacing: 0.125em;
  }

  40% {
    opacity: 1;
    transform: translateX(-1.5em);
  }

  50% {
    transform: translateX(-0.1em);
    letter-spacing: 0.5em;
  }

  70% {
    opacity: 1;
    transform: translateX(-0.5em);
  }

  100% {
    opacity: 0;
  }
}

.anim-button {
  animation-name: button-anim;
  animation-duration: 3s;
  animation-delay: 2s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

@keyframes button-anim {
  0% {
    transform: rotate(0deg);
  }

  6% {
    transform: rotate(-30deg);
  }

  15% {
    transform: rotate(10deg) scale(0.9, 0.9);
  }

  20% {
    transform: rotate(-5deg);
  }

  35% {
    transform: rotate(2deg) scale(1, 1);
    box-shadow: 2px 2px 10px alpha($color2, 0.8);
    color: $color2;
    border-color: $color2;
  }

  50% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(0deg);
  }
}
</style>
