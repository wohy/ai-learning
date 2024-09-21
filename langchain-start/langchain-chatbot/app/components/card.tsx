import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default function BackgroundBlogCard(props: { title: string, content: string }) {
  return (
    <Card sx={{ width: 235 }}>
        <CardContent>
          {props.title ? <Typography gutterBottom variant="h5" component="div">
            {props.title}
          </Typography> : null}
          {props.content ? <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            {props.content}
          </Typography> : null}
        </CardContent>
    </Card>
  );
}