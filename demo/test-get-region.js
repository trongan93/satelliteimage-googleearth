
// Define a function that will make a rectangle from a center point
// based on x and y extension distance and projection parameters.
function makeRectangle(point, xRadius, yRadius, proj) {
  var pointLatLon = ee.Geometry.Point(point);
  var pointMeters = pointLatLon.transform(proj, 0.001);
  var coords = pointMeters.coordinates();
  var minX = ee.Number(coords.get(0)).subtract(xRadius);
  var minY = ee.Number(coords.get(1)).subtract(yRadius);
  var maxX = ee.Number(coords.get(0)).add(xRadius);
  var maxY = ee.Number(coords.get(1)).add(yRadius);
  var rect = ee.Geometry.Rectangle([minX, minY, maxX, maxY], proj, false);
  return rect;
}

// Define inputs for making a rectangle from center point.
var point = [-122.0522, 37.00704];  // lat, lon
var xRadius = 50; // meters
var yRadius = 50; // meters
var proj = 'EPSG:3310'; // California Albers Equal Area projection

// Make a rectangle from center point.
var rect = makeRectangle(point, xRadius, yRadius, proj);

// Show the retangle and point.
Map.setOptions('SATELLITE');
Map.centerObject(rect, 17);
Map.addLayer(rect, {color: 'blue'}, 'Rectangle');
Map.addLayer(ee.Geometry.Point(point), {color: 'yellow'}, 'Point');

// Print some info about the rectangle.
print(rect.area(0.001)); // Should be 10,000
print(rect.perimeter(0.001)); // Should be 400
print(rect.length());
print(rect.coordinates());
