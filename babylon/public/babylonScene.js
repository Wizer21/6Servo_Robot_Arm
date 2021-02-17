const createScene =  () => {
    const scene = new BABYLON.Scene(engine);
    const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, new BABYLON.Vector3(0, 0, 25));
    camera.attachControl(canvas, true);
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0));
	const box = BABYLON.MeshBuilder.CreateBox("box", {});
    const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: 50, width: 50, subdivisions: 4});
	
	BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/models/", "chair.obj", scene, function (newMeshes) {
	});
	BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/models/", "Campfire.obj", scene, function (newMeshes) {
		//newMeshes[0].position.x = 0.01;
        var fire = newMeshes[0].getChildMeshes()[0];
        newMeshes.x = 2
	});
    return scene;
}

