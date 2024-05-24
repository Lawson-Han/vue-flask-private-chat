<template>
  <div>
    <div
      v-if="msg.from.name === this.username"
      class="chat__mymessage"
      :class="[isSame ? '' : 'chat__first']"
    >
      <div>
        <p class="chat__mymessage__user" v-if="!isSame">
          {{ msg.from.name }}
        </p>
        <div class="chat__yourmessage__p">
          <p class="chat__mymessage__paragraph">{{ msg.msg }}</p>
          <!-- <p class="chat__yourmessage__time">23:38</p> -->
        </div>
      </div>
      <!-- <p class="chat__yourmessage__time">23:38</p> -->
<!--      <p class="chat__mymessage__paragraph">{{ msg.msg }}</p>-->
    </div>
    <div
      v-else
      class="chat__yourmessage"
      :class="[isSame ? '' : 'chat__first']"
    >
      <div>
        <p class="chat__yourmessage__user" v-if="!isSame">
          {{ msg.from.name }}
        </p>
        <div class="chat__yourmessage__p">
          <p class="chat__yourmessage__paragraph">
            {{ msg.msg }}
          </p>
          <!-- <p class="chat__yourmessage__time">23:38</p> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['msg', 'prev', 'username'],
  data () {
    return {
      isSame: false
    }
  },
  methods: {
    isSamePerson (msg, prev) {
      // console.log(msg?.from.name, prev[0]?.from.name)
      if (prev === null) {
        return false
      } else if (prev[0]?.from.name === msg?.from.name) {
        return true
      } else {
        return false
      }
    }
  },
  created () {
    this.isSame = this.isSamePerson(this.msg, this.prev)
  }
}
</script>

<style>
.chat__mymessage {
  display: flex;
  justify-content: right;
  align-items: flex-end;
  margin: 0;
  min-height: 40px;
  line-break: anywhere;
}

.chat__mymessage__paragraph {
  margin: 0.4rem 0 1rem 0rem;
  border-radius: 20px 20px 0px 20px;
  max-width: 300px;
  background-color: #bbc4ef;
  color: #ffffff;
  padding: 0.8rem;
  font-size: 14px;
}

.chat__first {
  margin-top: 2rem;
}

.chat__yourmessage {
  display: flex;
}

.chat__yourmessage__avartar {
  width: 40px;
  margin-right: 1rem;
}

.chat__yourmessage__img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.chat__mymessage__user {
  display: flex;
  justify-content: right;
  align-items: flex-end;
  font-size: 14px;
  font-weight: 700;
  color: #292929;
  margin-block-end: 0rem;
}

.chat__yourmessage__user {
  font-size: 14px;
  font-weight: 700;
  color: #292929;
  margin-top: 0;
  margin-block-end: 0rem;
}

.chat__yourmessage__p {
  display: flex;
  align-items: flex-end;
  line-break: anywhere;
}

.chat__yourmessage__paragraph {
  margin: 0.4rem 1rem 0 0;
  border-radius: 0px 20px 20px 20px;
  background-color: #f3f3f3;
  max-width: 300px;
  color: #414141;
  padding: 0.8rem;
  font-size: 14px;
}

.chat__yourmessage__time {
  margin: 0;
  font-size: 12px;
  color: #9c9c9c;
}
</style>
