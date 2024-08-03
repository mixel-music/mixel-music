function getCoverUrl(hash: string | undefined, size?: number): string {
  let coverUrl: string =
    `http://localhost:2843/api/artwork/${ hash }${ size ? `?size=${ size.toString() }` : '' }`;

  return coverUrl;
}

function getFormattedTime(time: number): string {
  const min = Math.floor(time / 60);
  const sec = Math.floor(time % 60);

  return `${ min }:${ sec < 10 ? '0' : '' }${ sec }`;
}

export {
  getCoverUrl,
  getFormattedTime,
}