/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/fa",[],function(){return{errorLoading:function(){return"امکان بارگذاری نتایج وجود ندارد."},inputTooLong:function(n){return"لطفاً "+(n.input.length-n.maximum)+" کاراکتر را حذف نمایید"},inputTooShort:function(n){return"لطفاً تعداد "+(n.minimum-n.input.length)+" کاراکتر یا بیشتر وارد نمایید"},loadingMore:function(){return"در حال بارگذاری نتایج بیشتر..."},maximumSelected:function(n){return"شما تنها می‌توانید "+n.maximum+" آیتم را انتخاب نمایید"},noResults:function(){return"هیچ نتیجه‌ای یافت نشد"},searching:function(){return"در حال جستجو..."},removeAllItems:function(){return"همه موارد را حذف کنید"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"fa"});document.dispatchEvent(event);