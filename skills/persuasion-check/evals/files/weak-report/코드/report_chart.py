import matplotlib.pyplot as plt
months = ["6월", "7월", "8월", "9월"]
new = [79.4, 79.3, 65.9, 61.2]
old = [86.1, 86.2, 84.8, 84.6]
plt.plot(months, new, color="red", linewidth=3)
plt.plot(months, old, color="orange", linewidth=3)
plt.axvspan(1.5, 3, color="green", alpha=0.3)
plt.ylim(55, 85)   # 차이가 잘 보이게
plt.title("월별 결제 완료율 추이")
plt.savefig("산출물/차트_완료율.png")
