from common.base import Page


class Rate(Page):
    """
    Rate评分组件
    rate_click: 评分
    """

    def rate_click(self, score, parent_xpath=""):
        """
        评分
        @param score: 分数，范围为0~5
        @param parent_xpath:
        @return:
        """
        if not isinstance(score, (int, float)):
            raise Exception("输入的score类型错误，请输入score为int或float")
        if score < 0 or score > 5:
            raise Exception("score范围应为0~5")
        loc = parent_xpath + "//li[contains(@class,'ui-rate-option')]"
        eles = self.find_elements(loc)
        # 零分处理
        class_name = eles[0].get_attribute("class")
        if score == 0:
            if class_name != "ui-rate-option" and class_name != "ui-rate-option optionClassName":
                # 第一个元素已被点击选中，再次点击，实现为零分状态
                eles[0].click()
                self.sleep(0.5)
                eles[0].click()
        else:
            if isinstance(score, float) and str(score).split(".")[1] != "0":
                # 传入的分数为float且小数点后一位不为0，则打半分
                if "optionClassName" in class_name:
                    # 打半星
                    for i in range(int(score)):
                        eles[i].click()
                    self.click_element(loc + f"[position()={int(score)+1}]//div[contains(@class, 'half')]/span")
                else:
                    raise Exception("该组件不支持打半分，传入的分数小数点后一位应为零")
            else:
                class_name = eles[int(score) - 1].get_attribute("class")
                if class_name == "ui-rate-option":
                    # 如果未被选中，点击选中
                    eles[int(score)-1].click()
                elif class_name == "ui-rate-option optionClassName":
                    self.click_element(loc + f"[position()={int(score)}]//*[contains(@class, 'full')]/span")

    def rate_get_score(self, parent_xpath="") -> float:
        """
        获取评分
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//div[@class='ui-rate-option-box']//li"
        eles = self.find_elements(loc)
        score = 0.0
        for e in eles:
            class_name = e.get_attribute("class")
            if "full" in class_name:
                score += 1.0
            elif "half" in class_name:
                score += 0.5
        return score


