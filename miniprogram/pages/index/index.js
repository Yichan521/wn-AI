const { envList } = require("../../envList");
const { QuickStartPoints, QuickStartSteps } = require("./constants");

Page({
  data: {
    knowledgePoints: QuickStartPoints,
    steps: QuickStartSteps,
  },

  copyCode(e) {
    const code = e.target?.dataset?.code || "";
    wx.setClipboardData({
      data: code,
      success: () => {
        wx.showToast({
          title: "已复制",
        });
      },
      fail: (err) => {
        console.error("复制失败-----", err);
      },
    });
  },

  discoverCloud() {
    wx.switchTab({
      url: "/pages/examples/index",
    });
  },

  gotoGoodsListPage() {
    wx.navigateTo({
      url: "/pages/goods-list/index",
    });
  },

  onCard1Tap() {
    wx.showToast({
      title: "智能文案生成",
      icon: "none",
    });
  },

  onCard2Tap() {
    wx.showToast({
      title: "数字人视频制作",
      icon: "none",
    });
  },

  onCard3Tap() {
    wx.showToast({
      title: "AI营销海报设计",
      icon: "none",
    });
  },

  gotoWrittingPage() {
    wx.navigateTo({
      url: "/pages/writting/index",
    });
  },
});
