var canvas = document.getElementById("renderCanvas");

var createScene = function () {
    const scene = new BABYLON.Scene(engine);

	const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, new BABYLON.Vector3(0, 0, 0), scene);
	camera.attachControl(canvas, true);
	const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
	//const box = BABYLON.MeshBuilder.CreateBox("box", {}, scene);

	BABYLON.SceneLoader.ImportMeshAsync("city", ".//models/", "city.obj", scene).then((result) => {
		result.meshes[1].position.x = 20;
		const mesh1 = scene.getMeshByName("city");
	});

	return scene;
};

var engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
var scene = createScene();

   engine.runRenderLoop(function () {
	if (scene) {
		scene.render();
	}
});

// Resize
window.addEventListener("resize", function () {
	engine.resize();
});
