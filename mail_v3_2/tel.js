// JavaScript Document
$(function() {
  $('.tel').each(function() {
//.tel内のHTMLを取得
    var str = $(this).html();
//子要素がimgだった場合、alt属性を取得して電話番号リンクを追加
    if ($(this).children().is('img')) {
      $(this).html($('<a>').attr('href', 'tel:' + $(this).children().attr('alt').replace(/-/g, '')).append(str + '</a>'));
    } else {
//それ以外はテキストを取得して電話番号リンクを追加
      $(this).html($('<a>').attr('href', 'tel:' + $(this).text().replace(/-/g, '')).append(str + '</a>'));
    }
  });
});