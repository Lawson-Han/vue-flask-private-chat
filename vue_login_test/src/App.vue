<template>
  <div id="app">
    <vue-particles
        color="#555"
        :particleOpacity="0.7"
        :particlesNumber="120"
        shapeType="circle"
        :particleSize="4"
        linesColor="#555"
        :linesWidth="1"
        :lineLinked="true"
        :lineOpacity="0.4"
        :linesDistance="150"
        :moveSpeed="2"
        :hoverEffect="true"
        hoverMode="grab"
        :clickEffect="true"
        clickMode="push"
        class="test_"
      >
    </vue-particles>
    <!-- 路由占位符 -->
    <router-view/>
  </div>
</template>

<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css");
@font-face {
  font-family: "Golden Plains - Demo";
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

* {
  font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto,
    "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR",
    "Malgun Gothic", sans-serif;
}

body {
    width: 100%;
    background-color: rgb(239, 239, 239);
  }
  .test_{
    position: fixed;
    top: 0;
    width: 100%;
  }

.container {
  max-width: 900px;
  background-color: #ffffff;
  margin-left: 25%;
  box-shadow: 0px 1px 20px #9c9cc855;
}

</style>
