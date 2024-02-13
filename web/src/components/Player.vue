<template>
  <div class="player">
    <div class="player-left">
      <p class="text-title" v-bind="{ title: Title }">{{ Title }}</p>
      <p class="text-description" v-bind="{ title: Artist + ' - ' + Album }" v-if="Title">{{ Artist }} - {{ Album }}</p>
      <p class="text-description" v-bind="{ title: LengthNowFormatted + ' / ' + LengthFormatted }" v-if="Title">{{ LengthNowFormatted }} / {{ LengthFormatted }}</p>
    </div>
    <div class="player-center">
      <button class="player-button" title="Previous" @click="PreviousTrack">
        <IconamoonPlayerStartFill />
      </button>
      <button class="player-button player-button-primary" v-bind="{ title: IsPlayNow ? 'Pause' : 'Play' }" @click="ToggleTrack">
        <IconamoonPlayerPauseFill v-if="IsPlayNow" />
        <IconamoonPlayerPlayFill v-else="IsPlayNow" />
      </button>
      <button class="player-button" title="Next" @click="NextTrack">
        <IconamoonPlayerEndFill />
      </button>
      <div class="player-range" @click="LengthSeek($event)" @mousedown="LengthDragStart($event)" @mouseup="DragStop">
        <div class="player-range-length">
          <div class="player-range-now" :style="{ 'width': LengthRangeValue + '%' }"></div>
        </div>
      </div>
    </div>
    <div class="player-right">
      <div class="player-volume" @mouseover="this.VolumeNowEnable = true" @mouseleave="this.VolumeNowEnable = false">
        <Transition name="ElementFade">
          <div class="player-range" v-bind="{ title: VolumeRangeValue + '%' }" v-if="(VolumeNowEnable || !IsLengthDragNow && IsDragNow)" @click="VolumeSeek($event)" @mousedown="VolumeDragStart($event)" @mouseup="DragStop">
            <div class="player-range-volume">
              <div class="player-range-now" :style="{ 'width': VolumeRangeValue + '%' }"></div>
            </div>
          </div>
        </Transition>
        <button class="player-button" title="Volume" @click="MuteTrack">
          <IconamoonVolumeOff v-if="this.Music.muted" />
          <IconamoonVolumeUp v-else-if="VolumeRangeValue >= 50" />
          <IconamoonVolumeDown v-else-if="VolumeRangeValue < 50" />
        </button>
      </div>
      <button class="player-button" v-bind="{ title: Repeat == 0 || Repeat == 1 ? 'Repeat' : 'Repeat one' }" :class="{ 'button-disabled': Repeat == 0 }" @click="RepeatTracks()">
        <IconamoonPlaylistRepeatList v-if="Repeat == 0 || Repeat == 1"/>
        <IconamoonPlaylistRepeatSong v-else />
      </button>
      <button class="player-button" title="Shuffle" :class="{ 'button-disabled': !Shuffle }" @click="Shuffle = true">
        <IconamoonPlaylistShuffle />
      </button>
      <button class="player-button" title="Play queue">
        <IconamoonPlaylist />
      </button>
    </div>
  </div>
</template>

<script>
import IconamoonPlayerPauseFill from '~icons/iconamoon/player-pause-fill';
import IconamoonPlayerPlayFill from '~icons/iconamoon/player-play-fill';
import IconamoonPlayerStartFill from '~icons/iconamoon/player-start-fill';
import IconamoonPlayerEndFill from '~icons/iconamoon/player-end-fill';

import IconamoonVolumeUp from '~icons/iconamoon/volume-up';
import IconamoonVolumeDown from '~icons/iconamoon/volume-down';
import IconamoonVolumeOff from '~icons/iconamoon/volume-off';

import IconamoonPlaylistRepeatList from '~icons/iconamoon/playlist-repeat-list';
import IconamoonPlaylistRepeatSong from '~icons/iconamoon/playlist-repeat-song';
import IconamoonPlaylistShuffle from '~icons/iconamoon/playlist-shuffle';
import IconamoonPlaylist from '~icons/iconamoon/playlist';

import IconamoonHeart from '~icons/iconamoon/heart';
import IconamoonHeartFill from '~icons/iconamoon/heart-fill';
import IconamoonMenuKebabHorizontal from '~icons/iconamoon/menu-kebab-horizontal';

export default {
  components: {
    IconamoonPlayerPauseFill,
    IconamoonPlayerPlayFill,
    IconamoonPlayerStartFill,
    IconamoonPlayerEndFill,

    IconamoonVolumeUp,
    IconamoonVolumeDown,
    IconamoonVolumeOff,

    IconamoonPlaylistRepeatList,
    IconamoonPlaylistRepeatSong,
    IconamoonPlaylistShuffle,
    IconamoonPlaylist,

    IconamoonHeart,
    IconamoonHeartFill,
    IconamoonMenuKebabHorizontal,
  },

  data() {
    return {
      Music: new Audio(),
      Title: null,
      Album: null,
      Artist: null,

      Length: 0, // RAW Value (sec, float)
      LengthNow: 0, // RAW Value (sec, float)

      VolumeNow: 1, // RAW Value (0~1)
      VolumeNowEnable: false,

      Repeat: 0,
      Shuffle: false,

      IsDragNow: false,
      IsLengthDragNow: false,
      IsPlayNow: false,
    }
  },

  created() {
    this.Music.addEventListener('timeupdate', this.UpdateTime);
    this.Music.addEventListener('loadedmetadata', () => {
      this.Length = this.Music.duration;
    });
  },

  beforeUnmount() {
    this.Music.removeEventListener('timeupdate', this.UpdateTime);
    this.Music.removeEventListener('loadedmetadata', () => {
      this.Length = this.Music.duration;
    });
    this.Music.removeEventListener('ended', this.HandleMusicEnd);
    this.Music.pause();

    if (this.IsDragNow) {
      document.removeEventListener('mousemove', this.LengthDrag);
      document.removeEventListener('mousemove', this.DragStart);
      document.removeEventListener('mousemove', this.DragStop);
    }
  },

  mounted() {
    this.Music.addEventListener('ended', this.HandleMusicEnd);
  },

  computed: {
    LengthNowFormatted() {
      return this.FormatTime(this.LengthNow);
    },

    LengthFormatted() {
      return this.FormatTime(this.Length);
    },

    LengthRangeValue() {
      return (this.LengthNow / this.Length * 100).toFixed(2); // Formatted(int), 0 to 100
    },

    VolumeRangeValue() {
      return Math.floor(this.VolumeNow * 100); // Formatted(int), 0 to 100
    },
  },

  methods: {
    SelectTrack(title, album, artist, path) {
      this.Title = title;
      this.Album = album;
      this.Artist = artist;
      this.Music.src = `http://localhost:8000/api/stream/${path}`;

      if (this.Music.paused) {
        this.Music.play();
        this.IsPlayNow = true;
        this.SetMediaControls();
      }
    },
    
    SetMediaControls: function () {
      if ('mediaSession' in navigator) {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: this.Title,
          album: this.Album,
          artist: this.Artist,
          artwork: [],
        });

        navigator.mediaSession.setActionHandler("play", () => { this.ToggleTrack(); });
        navigator.mediaSession.setActionHandler("pause", () => { this.ToggleTrack(); });
        navigator.mediaSession.setActionHandler("seekbackward", () => { this.Music.currentTime -= 10; });
        navigator.mediaSession.setActionHandler("seekforward", () => { this.Music.currentTime += 10; });
        navigator.mediaSession.setActionHandler("previoustrack", () => { this.PreviousTrack();});
        navigator.mediaSession.setActionHandler("nexttrack", () => { this.NextTrack(); });
      }
    },

    UpdateTime() {
      if (!this.IsDragNow) this.LengthNow = this.Music.currentTime;
      this.MusicSlider = (this.MusicCurrent / this.MusicDuration) * 100;
      if (!this.IsDrag && this.MusicCurrent >= this.MusicDuration) {
        this.resetPlayer();
      }
    },

    FormatTime(time) {
      const min = Math.floor(time / 60);
      const sec = Math.floor(time % 60);
      return `${min}:${sec < 10 ? '0' : ''}${sec}`;
    },

    PreviousTrack() {
      this.Music.currentTime = 0;
    },

    ToggleTrack() {
      if (!this.IsDragNow && this.Music.paused && this.LengthNow >= this.Length && this.LengthNow != 0) {
        this.LengthNow = 0;
        this.Music.play();
        this.IsPlayNow = true;
        this.SetMediaControls();
      }
      else if (this.Music.paused) {
        if (this.Music.src) {
          this.Music.play();
          this.IsPlayNow = true;
          this.SetMediaControls();
        }
        else {
          console.warn("DEBUG: Select any tracks to play");
        }
      }
      else {
        this.Music.pause();
        this.IsPlayNow = false;
        this.SetMediaControls();
      }
    },

    NextTrack() {
      console.log("Test");
    },

    HandleMusicEnd() {
      if (!this.IsDragNow) {
        this.IsPlayNow = false;
        this.Music.pause();
        this.SetMediaControls();
      }
    },

    HandleRangeMove(event, RangeClass, callback) {
      const Range = this.$el.querySelector(RangeClass);
      const RangeWidth = Range.clientWidth;
      const MouseLocation = event.clientX - Range.getBoundingClientRect().left;
      const NewRangeValue = MouseLocation / RangeWidth;
      callback(NewRangeValue);
    },

    LengthSeek(event) {
      this.HandleRangeMove(event, '.player-range-length', value => {
        this.Music.currentTime = value * this.Length;
        this.LengthNow = this.Music.currentTime;
      });
    },

    VolumeSeek(event) {
      this.HandleRangeMove(event, '.player-range-volume', value => {
        this.Music.volume = Math.min(Math.max(value, 0), 1);
        this.VolumeNow = this.Music.volume;
        if (this.VolumeNow != 0) {
          this.Music.muted = false;
        }
        else {
          this.Music.muted = true;
        }
      });
    },
    
    LengthDragStart(event) {
      if(this.IsPlayNow) {
        this.IsDragNow = true;
        this.IsLengthDragNow = true;
        document.addEventListener('mousemove', this.LengthDragStart);
        document.addEventListener('mouseup', this.DragStop);
        this.HandleRangeMove(event, '.player-range-length', value => {
          this.LengthNow = Math.min(Math.max(value * this.Length, 0), this.Music.duration - 0.1);
          this.Music.currentTime = this.LengthNow;
        });
      }
    },

    VolumeDragStart(event) {
      this.IsDragNow = true;
      document.addEventListener('mousemove', this.VolumeDragStart);
      document.addEventListener('mouseup', this.DragStop);
      this.HandleRangeMove(event, '.player-range-volume', value => {
        this.Music.volume = Math.min(Math.max(value, 0), 1);
        this.VolumeNow = this.Music.volume;
        if (this.VolumeNow != 0) {
          this.Music.muted = false;
        }
        else {
          this.Music.muted = true;
        }
      });
    },

    DragStop() {
      this.IsDragNow = false;
      this.IsLengthDragNow = false;
      document.removeEventListener('mousemove', this.LengthDragStart);
      document.removeEventListener('mousemove', this.VolumeDragStart);
      document.removeEventListener('mouseup', this.DragStop);
    },

    MuteTrack() {
      if (this.Music.muted) {
        this.Music.muted = false;
        if (this.Music.volume == 0) {
          this.VolumeNow = this.Music.volume = 0.1;
        }
        else {
          this.VolumeNow = this.Music.volume;
        }
      }
      else {
        this.Music.muted = true;
        this.VolumeNow = 0;
      }
    },

    RepeatTracks() {
      if (this.Repeat == 0) {
        this.Repeat = 1;
        this.Music.loop = true;
      }
      else if (this.Repeat == 1) {
        this.Repeat = 2;
        this.Music.loop = true;
      }
      else {
        this.Repeat = 0;
        this.Music.loop = false;
      }
    },
  }
}
</script>
