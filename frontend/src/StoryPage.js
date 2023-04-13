import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function StoryPage() {
  const [story, setStory] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [audioURL, setAudioURL] = useState(null);

  const { storyId } = useParams();

  useEffect(() => {
    axios.get(`https://your-api-url.com/stories/${storyId}`)
      .then((response) => {
        setStory(response.data.story);
        setImageURL(response.data.imageUrl);
        setAudioURL(response.data.audioUrl);
      });
  }, [storyId]);

  if (!story) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <img src={imageURL} alt="Story" />
      <h1>{story.title}</h1>
      <p>{story.text}</p>
      <audio controls>
        <source src={audioURL} type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}

export default StoryPage;
