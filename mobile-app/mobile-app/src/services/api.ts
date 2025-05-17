export const uploadPhoto = async (uri: string, osNumber: string) => {
  const formData = new FormData();

  formData.append("os_number", osNumber);
  formData.append("file", {
    uri,
    name: `photo_${Date.now()}.jpg`,
    type: 'image/jpeg',
  } as any); // ⚠️ o "as any" ajuda a evitar erro de tipo no React Native

  try {
    const response = await fetch("http://192.168.1.66:8000/upload-photo/", {
      method: "POST",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      body: formData,
    });

    const json = await response.json();
    console.log("✅ Enviado com sucesso:", json);
    return json;
  } catch (error) {
    console.error("❌ Erro ao enviar a foto:", error);
    throw error;
  }
};
