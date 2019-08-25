{% load tests %}{# javascript to render 'widget.html' in browser #}
(function(){
  'use strict';
  function resizeIFrameToFitContent( iFrame ) {
    iFrame.width  = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
  }

  window.addEventListener('DOMContentLoaded', function(e) {

    var iFrame = document.getElementById( 'article-widget-frame' );
    resizeIFrameToFitContent( iFrame );

    // or, to resize all iframes:
    var iframes = document.querySelectorAll("iframe");
    for( var i = 0; i < iframes.length; i++) {
        resizeIFrameToFitContent( iframes[i] );
    }
} );

  // remove anchor tag after get url path
  var atag = document.getElementsByClassName('widget-embed');
  var username = atag[0].dataset.ghUsername;
  atag[0].style.display = 'none';     // anchor disappears

  // create <iframe>を
  var iframe = document.createElement('iframe');
  iframe.scrolling = 'no';
  iframe.frameBorder = 0;
  iframe.marginWidth = 0;
  iframe.marginHeight = 0;
  iframe.width = '100%';
  iframe.height = '100%';
  iframe.id = 'article-widget-frame';

  // insert iframe to the atag
  atag[0].parentNode.insertBefore(iframe,atag[0]);

  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (req.readyState == 4) { // http complete
      if (req.status == 200) { // http response success
          var doc = iframe.contentWindow.document;
          doc.open();
          doc.write(req.responseText);
          doc.close();
      }
    }
  }
  req.open('GET', '{% fullurl "mylinks_oembed_widget" id=instance.id content_type=content_type %}');
  req.send(null);
})();
