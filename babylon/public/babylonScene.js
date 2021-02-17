const createScene =  () => {
    const scene = new BABYLON.Scene(engine);
    const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, new BABYLON.Vector3(0, 0, 25));
    camera.attachControl(canvas, true);
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0));
    
    const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: 50, width: 50, subdivisions: 4});
	
	// BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/models/", "chair.obj", scene, function (newMeshes) {
    //     console.log("in chair")
    //     var chair = newMeshes[0];
    //     chair.scaling = new BABYLON.Vector3(4, 4, 4);
    //     chair.position = new BABYLON.Vector3(4, 4, 4);
	// });

	// BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/models/", "Campfire.obj", scene, function (newMeshes) {
    //     console.log("in camp")
    //     console.log(newMeshes)
    //     var campfire = newMeshes[0];
    //     campfire.scaling = new BABYLON.Vector3(0.5, 0.5, 0.5);
    //     campfire.position = new BABYLON.Vector3(2, 2, 2);
	// });

    const box = BABYLON.MeshBuilder.CreateBox("box", {height: 2, width: 2, depth: 2}, scene);
    const box1 = BABYLON.MeshBuilder.CreateBox("box1",{height: 1, width: 2, depth: 1}, scene);

    box1.position = new BABYLON.Vector3(2, 2, 2);

    var groundMaterial = new BABYLON.StandardMaterial("ground", scene);
    // BACKGROUND
    var hdrTexture = new BABYLON.CubeTexture("/textures/SpecularHDR.dds", scene);
    scene.createDefaultSkybox(hdrTexture, true, 10000);
    

    return scene;
}

